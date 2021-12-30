---
layout: post
title: bootstrap
categories: 网页
description: 
---

{:toc}
[[网页]]
## 什么是bootstrap
1. 快速开发页面
2. 响应式布局

## 容器

所有的布局都要在容器中

`.container` 类用于固定宽度并支持响应式布局的容器。

```html
<div class="container">
  ...
</div>
```

`.container-fluid` 类用于 100% 宽度，占据全部视口（viewport）的容器。

```html
<div class="container-fluid">
  ...
</div>
```

##  栅格
一共12列

```
 <div class="row">

 <div class="col-md-1">.col-md-1</div>

 <div class="col-md-1">.col-md-1</div>

 <div class="col-md-1">.col-md-1</div>

 <div class="col-md-1">.col-md-1</div>

 <div class="col-md-1">.col-md-1</div>

 
 <div class="col-md-1 col-md-offset-3" >.col-md-1</div>

 <div class="col-md-1">.col-md-1</div>

 </div>
```

col-md-offset 用作偏移


## css
```
1. lead  段落字体变大
2. <mark> 高亮
3. <del> 删除
4. <u> 下划线
5. <strong> 加粗
6. <code> 代码
7. <pre> 代码块
```


####  对齐
```html
<p class="text-left">Left aligned text.</p>
<p class="text-center">Center aligned text.</p>
<p class="text-right">Right aligned text.</p>
```

#### 改变大小写
```html
<p class="text-lowercase">Lowercased text.</p>
<p class="text-uppercase">Uppercased text.</p>
<p class="text-capitalize">Capitalized text.</p>
```


## 表格
### 条纹状表格
> .table-striped


### 带边框的表格
> .table-bordered

