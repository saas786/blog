---
layout: post
title: tablayout的复习
categories: android
description:  tabLayout,tab,tabview和tabItem的关系你了解吗
---

{:toc}

### 基础认知
首先认知对tablayout进行一个基础认知:
一个可以横向滚动的layout
```
public class TabLayout extends HorizontalScrollView
```

### 基础用法

#### 用法1
```
 TabLayout tabLayout = ...;
 tabLayout.addTab(tabLayout.newTab().setText("Tab 1"));
 tabLayout.addTab(tabLayout.newTab().setText("Tab 2"));
 tabLayout.addTab(tabLayout.newTab().setText("Tab 3"));
```

#### 用法2
```
<com.google.android.material.tabs.TabLayout
         android:layout_height="wrap_content"
         android:layout_width="match_parent">

     <com.google.android.material.tabs.TabItem
             android:text="@string/tab_text"/>

     <com.google.android.material.tabs.TabItem
             android:icon="@drawable/ic_android"/>

 </com.google.android.material.tabs.TabLayout>
```


### 和viewpager联动

#### setupWithViewPager
viewpager也可以横向滚动[setupWithViewPager](https://developer.android.google.cn/reference/com/google/android/material/tabs/TabLayout#setupWithViewPager(androidx.viewpager.widget.ViewPager)

####  布局上直接关联

```
 <androidx.viewpager.widget.ViewPager
       android:layout_width="match_parent"
       android:layout_height="match_parent">
  
       <com.google.android.material.tabs.TabLayout
           android:layout_width="match_parent"
           android:layout_height="wrap_content"
           android:layout_gravity="top" />
  
   </androidx.viewpager.widget.ViewPager>
```


#### 测试1
  
  如果tablayout是一个横向滚动的layout,那么里面不放tabItem,而是textview呢?
  
errror:
Only TabItem instances can be added to TabLayout

答:tabItem是官方认知存放在tabLayout中的视图.

代码也很简单

```
public class TabItem extends View {  
widget migration  
 public final CharSequence text;  

 public final Drawable icon;  

 public final int customLayout;  
  
 public TabItem(Context context) {  
    this(context, null);  
 }  
  
  public TabItem(Context context, AttributeSet attrs) {  
    super(context, attrs);  
  
 final TintTypedArray a =  
        TintTypedArray.obtainStyledAttributes(context, attrs, R.styleable.TabItem);  
 text = a.getText(R.styleable.TabItem_android_text);  
 icon = a.getDrawable(R.styleable.TabItem_android_icon);  
 customLayout = a.getResourceId(R.styleable.TabItem_android_layout, 0);  
 a.recycle();  
 }  
}
```

#### 测试2:tab
 通过tab设置相关参数创建tabLayout下的视图,或tabView或自定义的view.
 
 自定义的view判断在前所以有限.
 
 

