---
layout: post
title: kotlin下的fragment
categories: android
description:   kotlin下的fragment
keywords: 
---

本文转载于 [掘金-fundroid](https://juejin.cn/post/6989048326633029645)

[[android]]
{:toc}


1. FragmentFactory 的意义？
=======================

关于 Fragment 的使用约定
-----------------

有 Fragment 使用经验的人都知道，Fragment 必须有有一个空参的构造函数，否则编译时会出现一下错误：

```
This fragment should provide a default constructor (a public constructor with no arguments)
复制代码

```

但即使添加了空参的构造器，如果定义了任何带参数构造器，仍然会被亲切的提醒：

```
Avoid non-default constructors in fragments: use a default constructor plus Fragment#setArguments(Bundle) instead [ValidFragment]
复制代码

```

可见 Android 对于 Framgent 携带构造参数唯恐避之不及。

当系统发生 Configuration Change 时（例如横竖屏旋转等）Fragment 会恢复重建，此时系统不知道该选择哪个构造函数，所以系统与开发者约定，统一使用默认的空参构造函数构建，然后通过`setArgments`设置初始化值。

以往的处理方式：静态工厂
------------

为此，一个常见做法是通过静态方法，避免直接使用带参数的构造函数。

如下，静态方法 `getInstance(String str)` 中，先空参构造 Fragment，然后通过 `setArgments` 初始化。

```
public class MainFragment extends BaseFragment {

   private static final String MY_ARG = "my_arg";
   private String arg = "";

   public static MainFragment getInstance(String str) {
       MainFragment fragment = new MainFragment();
       Bundle bundle = new Bundle();
       bundle.putString(MY_ARG, str);
       fragment.setArguments(bundle);
       return fragment;
   }

   @Override
   public void onCreate(@Nullable Bundle savedInstanceState) {
       super.onCreate(savedInstanceState);
       if (getArguments() != null) {
           arg = getArguments().getString(MY_ARG);
       }
   }
}
复制代码

```

后续便可以使用此静态方法构建 Fragment 了

```
MainFragment fragment = MainFragment.getInstance("Hello world!!");
复制代码

```

Fragment 恢复重建过程中，系统会调用静态方法 `Fragment.instantiate`（在 `onCreate`和`onActivityCreated` 之间）

```
@NonNull
public static Fragment instantiate(@NonNull Context context, @NonNull String fname,
       @Nullable Bundle args) {
   try {
       Class extends Fragment> clazz = FragmentFactory.loadFragmentClass(
               context.getClassLoader(), fname);
       Fragment f = clazz.getConstructor().newInstance();
       if (args != null) {
           args.setClassLoader(f.getClass().getClassLoader());
           f.setArguments(args);
       }
       return f;
   } catch (java.lang.InstantiationException e) {
复制代码

```

我们先前通过 `setArguments` 传递的 `bundle`（随着 `onSaveInstanceState` 保存），会被系统传递给 `instantiate` ，以协助 fragment 的恢复重建。

新的处理方案：FragmentFactory
----------------------

以上关于 Fragment 空参构造函数的约定，随着 **androidx.fragment:fragment-1.1.0-alpha01** 的发布成为了历史。

新版本中 `Fragment.instantiate`已经被`@Deprecated`，推荐使用`FragmentManager.getFragmentFactory`和`FragmentFactory.instantiate (ClassLoader, String)`替代。FragmentFactory 允许开发者按照需要自由定义其构造函数，摆脱了空参构造的束缚。

2. FragmentFactory 如何使用？
========================

假设我们的 `MainFragment` 需要两个参数，那么使用 FragmentFactory 如何构造呢？

定义 FragmentFactory
------------------

首先，需要定义自己的 FragmentFactory 。主要是重写 `instantiate` 方法，注意跟以前比，已经不支持传入 Bundle args 作为参数了。即使你想使用 bundle 传参，也推荐在这里手动 setArgument ，而非借助系统的设置。

```
class MyFragmentFactory extends FragmentFactory {

   private final AnyArg anyArg1;
   private final AnyArg anyArg2;

   public MyFragmentFactory(AnyArg arg1, AnyArg arg2) {
       this.anyArg1 = arg1;
       this.anyArg2 = arg2;
   }

   @NonNull
   @Override
   public Fragment instantiate(@NonNull ClassLoader classLoader, @NonNull String className) {
       Class extends Fragment> clazz = loadFragmentClass(classLoader, className);
       if (clazz == MainFragment.class) {
          return new MainFragment(anyArg1, anyArg2);
       } else {
           return super.instantiate(classLoader, className);
       }
   }
}
复制代码

```

有了 FragmentFactory 的加持 Framgent 直接使用构造函数传参即可：

```
protected MainFragment(AnyArg arg1, AnyArg arg2) {
    this.arg1 = arg1;
    this.arg2 = arg2;
}
复制代码

```

设置 Factory
----------

接下来需要在 Activity 的`onCreate`中为 FragmentManager 设置此 Factory

```
MyFragmentFactory fragmentFactory = new MyFragmentFactory( someObject1,  someObject2);

@Override
public void onCreate(Bundle savedInstanceState) {
    getSupportFragmentManager().setFragmentFactory(fragmentFactory);
    super.onCreate(savedInstanceState);

      FragmentManager fragmentManager = getSupportFragmentManager();
      FragmentTransaction fragmentTransaction = fragmentManager.beginTransaction()
        .replace(
            R.id.fragment_container,
            MainFragment.class);
      if (addToBackStack) {
        fragmentTransaction.addToBackStack(tag);
      }
      fragmentTransaction.commit();

}
复制代码

```

后续 FragmentManager 在创建 / 恢复 fragment 时，会使用此 factory 创建实例。

> 需要特别注意的是，setFragmentFactory 一定要在`super.onCreate`之前调用，因为在 super.onCreate 中会进行 fragment 的重建是需要被使用到。

3. 应用场景：设置 LayoutId
===================

**androidx.annotation:annotation-1.1.0-alpha01** 起引入了`@ContentView` 注解用来为 Fragment 设置默认布局文件，但时隔不久，**androidx.fragment:fragment-1.1.0-alpha05** 起，`@ContentView` 从 class 注解变为构造函数注解，fragment 多了一个带参数的构造函数：支持使用构造函设置 LayoutId：

```
 /**
     * Alternate constructor that can be used to provide a default layout
     * that will be inflated by {@link #onCreateView(LayoutInflater, ViewGroup, Bundle)}.
     *
     * @see #Fragment()
     * @see #onCreateView(LayoutInflater, ViewGroup, Bundle)
     */
    @ContentView //以前是用在Class上的注解
    public Fragment(@LayoutRes int contentLayoutId) {
        this();
        mContentLayoutId = contentLayoutId;
    }
复制代码

```

> Note：Activity 自 androidx.activity:activity-1.0.0-alpha06 起也支持通过构造函数设置 LayoutId

构造函数中将传入的 LayoutId 存于`mContentLayoutId`，`onCreateView` 中根据 mConentLayoutId 自动创建 ContentView ：

```
    @Nullable
    public View onCreateView(@NonNull LayoutInflater inflater, @Nullable ViewGroup container,
            @Nullable Bundle savedInstanceState) {
        if (mContentLayoutId != 0) {
            return inflater.inflate(mContentLayoutId, container, false);
        }
        return null;
    }
复制代码

```

也就是说使用构造函数设置 LayoutId 就无需重写 onCreateView 了。

Fragment(@LayoutRes int contentLayoutId) + FragmentFactory
----------------------------------------------------------

你也许会问这跟 FragmentFactory 有什么关系呢?

因为这里使用了构造函数传递参数，当 ConfigurationChanged 发生时，默认调用无参构造函数进行 fragment 的恢复重建，`mContentLayoutId` 信息会丢失，onCreateView 无法正常创建视图。

因此当使用构造函数设置 LayoutId 时，如果要考虑恢复重建的场景，必须配套设置一个 FragmentFactory。可能是踩坑的人太多了，在 1.1.0 之后的 javadoc 中特别强调了这一点:

> You must set a custom FragmentFactory if you want to use a non-default constructor to ensure that your constructor is called when the fragment is re-instantiated.

所以，综合来看，你觉得通过构造函数设置 LayoutId 到底方不方便呢？

4. 应用场景： 依赖注入
=============

FragmentFactory 允许自定义构造参数创建 Fragment, 这在 dagger、koin 等 DI 框架的使用场景中也能发挥更大作用。

以 Koin 中 FragmentFactory 的使用为例 (对 Koin 的基本知识不做介绍):

```
//定义fragmentModules
private val fragmentModules = module {
    fragment { HomeFragment() }
    fragment { DetailsFragment(get()) } //通过get()获取依赖的参数
}
private val viewModelsModule = module {
    viewModel { DetailsViewModel(get()) }
}

//启动Koin
override fun onCreate() {
    super.onCreate()
    startKoin {
        androidContext(this@App)
        fragmentFactory() // 添加 KoinFragmentFactory
        loadKoinModules(listOf(viewModdules, fragmentModules, ...)) //装在fragmentModules
    }
}
复制代码

```

如上，`DetailsFrament` 参数依赖 `DetailsViewModel`

KoinFragmentFactory
-------------------

Koin 使用 `KoinFragmentFactory` 为其注入这个参数依赖, 其本质就是一个 `FragmentFactory`

```
class KoinFragmentFactory : FragmentFactory() {

    override fun instantiate(classLoader: ClassLoader, className: String): Fragment {
        val clazz = Class.forName(className).kotlin
        val instance = getKoin().getOrNull<Fragment>(clazz) //通过 Koin 创建 Fragment
        return instance ?: super.instantiate(classLoader, className)
    }

}
复制代码

```

> Koin 通过 KoinFragmentFactory 创建 Fragment，构造函数中允许有参数，可以通过 koin 的依赖注入获取

FragmentFactory 需要被设置到 FragmentManager 中使用。 KoinFragmentFactory 也同样。需要在 `Activity#onCreate` 或 `Fragment#onCreate` 中调用 `setupKoinFragmentFactory()`, 将其添加到当前 FragmentManager 中

```
override fun onCreate(savedInstanceState: Bundle?) {
    setupKoinFragmentFactory() // 设置到 FragmentManager
    super.onCreate(savedInstanceState)
    setContentView(R.layout.activity_main)
}
复制代码

```

```
fun FragmentActivity.setupKoinFragmentFactory(scope: Scope? = null) {
    if (scope == null) {
        supportFragmentManager.fragmentFactory = get()
    } else {
        supportFragmentManager.fragmentFactory = KoinFragmentFactory(scope)
    }
}
复制代码

```

需要注意，这个调用必须在 `super.onCreate` 之前完成，因为 `super.onCreate` 中会进行 fragment 的重建, 此时就需要用到 FragmentFactory 了

Koin 配置完成后，就可以想往常一样将 DetailFagment 添加到 Activity 中了

```
supportFragmentManager.beginTransaction()
    .replace(R.id.container, DetailsFragment::class.java, null)
    .commit()
复制代码

```

`FragmentTransaction` 会自动调用 `KoinFragmentFactory#instantiate()` 创建`DetailsFragment::class.java` 对应的 Fragment， 很方便吧？

