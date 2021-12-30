---
layout: post
title: compose的Textview
categories: compose
description: compose的第一课textview
---

compose搞起

{:toc}

[Compose 中的文字 ](https://developer.android.google.cn/jetpack/compose/text)




#### compose基础认知

1. 视图组件首字母大写
2. @Composable 创建视图组件
3.  @Preview(showBackground = true)   用于预览
4.  val context = LocalContext.current 获取context


## Textview


```
@Composable  
fun Greeting(name: String) {  
    Text(text = "Hello $name!", color = Color.Black, textAlign = TextAlign.Center)  
}
```


| 属性 | 作用 | 示例 |
| ---- | ---- | ---- |
|text|文本内容|"普通文本"|
|fontSize|字体大小|20.sp|
|fontFamily|字体|FontFamily.SasSerif|
|fontStyle|字体样式|FontStyle.Italic（斜体）|
|fontWeight|字体粗细|FontWeight.Medium|
|letterSpacing|字符间距|TextUnit.Sp(10)|
|textAlign|text显示样式|TextAlign.Justify(拉伸填充整个容器)|
|maxLines|最大显示行数|10|
|textDecoration|划线样式|TextDecoration.Underline(下划线)，TextDecoration.LineThrough（中划线）|
|style|text样式|TextStyle.Default|
|onTextLayout|文本计算完成回调|{}|
|overflow|文本溢出样式|TextOverflow.Ellipsis|


###  Modifier 所有的属性都可以控制

```
Text(  
    text = "Hello $name!", 
 	modifier = Modifier  
        .padding(10.dp)  
        .fillMaxWidth()  
        .height(100.dp)  
)
```

### AnnotatedString 富文本
```go
AnnotatedString.Builder().run {
				//设置单独的样式
                pushStyle(
                    SpanStyle(
                        color = Color.Blue,
                        fontSize = 30.sp,
                        fontStyle = FontStyle.Italic,
                        fontFamily = FontFamily.Cursive
                    )
                )
                append("四大名著")
                pop()//取消上面修改的样式对下文本的影响
                append("水浒传")
                append("三国演义")
                append("红楼梦")
                append("西游记")
                toAnnotatedString()
            }
```
---
```go
buildAnnotatedString {  
    withStyle(  
        style = SpanStyle(  
            color = Color.Red,  
            background = Color.White,  
            fontSize = 18.sp,  
            fontFamily = FontFamily.Monospace  
        )  
    ) {  
        append("Hello ")  
    }  
    append(" world")  
}
```

### 设置点击函数

```
val clickText = buildAnnotatedString {  
    pushStringAnnotation(tag = "tag_a", annotation = "https://devloper.android.com")  
    // 要添加注解的文本为"打开本文"  
    withStyle(  
        style = SpanStyle(  
            color = Color.Blue,  
            textDecoration = TextDecoration.Underline,  
            fontWeight = FontWeight.Bold  
        )  
    ) {  
        append("展示Android官网")  
    }  
    pop()  
  
}  
ClickableText(text = clickText) { int ->  
    clickText.getStringAnnotations(tag = "tag_a", start = int, end = int)  
        .firstOrNull()?.let { annotation ->  
            Toast.makeText(context, "官网: ${annotation.item}", Toast.LENGTH_LONG)  
                .show()  
        }
```

备注:以上还包含了pushStringAnnotation知识点

### 选择文字

默认情况下，可组合项不可选择，这意味着在默认情况下用户无法从您的应用中选择和复制文字。要启用文字选择，需要使用 [`SelectionContainer`](https://developer.android.google.cn/reference/kotlin/androidx/compose/foundation/text/selection/package-summary#SelectionContainer(androidx.compose.ui.Modifier,kotlin.Function0)) 可组合项封装文字元素：

      
```
@Composable

fun SelectableText() {

    SelectionContainer {

        Text("This text is selectable")

    }

}
```
### 设置不可选择

```
      

@Composable

fun PartiallySelectableText() {

    SelectionContainer {

        Column {

            Text("This text is selectable")

            Text("This one too")

            DisableSelection {

                Text("But not this one")

            }

            Text("But again, you can select this one")

            Text("And this one too")

        }

    }

}
```


## TextField 可编辑文字

在构建无需 Material 规范中的装饰的设计时，应使用 `BasicTextField`

 ```
       

@Composable

fun PasswordTextField() {

    var password by rememberSaveable { mutableStateOf("") }

  

    TextField(

        value = password,

        onValueChange = { password = it },

        label = { Text("Enter password") },

        visualTransformation = PasswordVisualTransformation(),

        keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Password)

    )

}
 ```

#### demo 连续删除三个清空
```
var input by remember { mutableStateOf("123456789") }  
var deleteNumber by remember { mutableStateOf(0) }  
var orginText by remember { mutableStateOf("123456789") }  
TextField(  
    value = input,  
    onValueChange = { newText ->  
        if (newText.length - orginText.length == -1) {  
            deleteNumber++  
        } else {  
            deleteNumber = 0  
        }  
        orginText = newText  
  
        input = if (deleteNumber == 3) {  
            ""  
        } else {  
            newText  
        }  
    }  
)
```

[[android]]