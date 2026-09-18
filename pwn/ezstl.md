# ezstl - WriteUp
> 本题知识点：  
> :star::star::star: STL内部代码的阅读能力
> :star::star: std::vector的内存结构  
> :star::star::star::star: C++虚函数与多态性的底层实现  

源码因篇幅太长而置于文末。

## `std::vector` 容器的内部结构
打开你的IDE（包括配置好插件的vscode），打开pwn.cpp，**Ctrl+左键** `std::vector` 跳转到 vector 的定义  
你会发现：`std::vector`中没有直接声明任何变量，只是一堆类型别名（typedef）  
于是继续追踪**父类** `_Vector_base`，发现内部声明了3个变量，部分代码如下  
```cpp
pointer _M_start;
pointer _M_finish;
pointer _M_end_of_storage;
```
> PS: 这里其实是`_Vector_base`中的一个内部结构体的3个字段  
经过一番研究，最终确定 `std::vector` 内部实际存着3个指针，
结合名称可知：  
- **_M_start**: 指向缓冲区的起始位置（类似栈底）
- **_M_finish**: 指向存储的最后一个数据（最后push_back的）（类似栈顶）
- **_M_end_of_storage**: 指向缓冲区的末尾

在 **x86_64** 架构下，3个指针各占8字节，即一个 `std::vector` 对象占据 **0x18** 个字节

## C++中的虚函数和多态性
此处假设你了解过一部分**多态性**，若不了解请戳[这里](https://zhuanlan.zhihu.com/p/1967019746835796329)  

### 虚表
我们都知道，通过多态性可以实现动态派发  
在C++中，多态性是通过**虚表 vtable**实现的  
虚表是一个**指针数组**，存放着**子类**的虚函数地址，以**nullptr**（0）结束  
同时C++会在每个拥有虚方法的对象中额外存储一个**虚表指针 vptr**来指向虚表  
当调用虚方法时，程序会从**vptr**一路追踪到子类的虚函数地址并调用  

### 一个简单的例子
```cpp
class A {
public:
    virtual void vfunc1();
    virtual void vfunc2();
    void func1();
    void func2();
private:
    int m_data1, m_data2;
};
```
`A`类中声明了2个虚函数，定义相关对象后在内存中的结构如下图所示：  
![虚表示意图](../assets/pwn_ezstl/vtable.jpg)  
**vptr**的位置因编译器而异，大多数情况位于对象的**首部**，在所有成员之前

> 以上示例来自于：https://zhuanlan.zhihu.com/p/75172640

## 源码
```cpp
#include <cstdio>
#include <cstdlib>
#include <unistd.h>
#include <vector>

class Badge {
public:
    virtual void show()
    {
        puts("guest badge");
    }
};

extern "C" void win()
{
    puts("admin badge");
    system("/bin/sh");
}

struct Profile {
    char name[0x30];
    std::vector<void *> styles;
    Badge badge;
};

struct StyleData {
    void *slot[1];
};

struct HeapData {
    Profile profile;
    StyleData custom_style;
};

void setup()
{
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);
    alarm(60);
}

unsigned long read_ulong()
{
    char buf[0x40] = {};
    size_t i = 0;

    while (i + 1 < sizeof(buf)) {
        char ch = 0;
        ssize_t n = read(0, &ch, 1);
        if (n <= 0) {
            exit(0);
        }
        if (ch == '\n') {
            break;
        }
        buf[i++] = ch;
    }

    return strtoul(buf, NULL, 0);
}

void add_style(Profile *profile, StyleData *style)
{
    profile->styles.push_back(style);
}

void check_badge(Badge *badge)
{
    badge->show();
}

int main()
{
    setup();

    HeapData *data = new HeapData;
    Profile *profile = &data->profile;
    StyleData *custom_style = &data->custom_style;

    puts("== pwn ==");
    printf("profile: %p\n", profile);
    // printf("style: %p\n", custom_style); // 注：这行代码在实际二进制文件中并不存在
                                            // 可能是出题人的疏忽

    printf("name: ");
    if (read(0, profile->name, 0x48) <= 0) {
        exit(0);
    }

    add_style(profile, custom_style);

    printf("win: %p\n", (void *)win);
    printf("style data: ");
    custom_style->slot[0] = (void *)read_ulong();

    puts("checking...");
    check_badge(&profile->badge);

    _exit(0);
}

```
