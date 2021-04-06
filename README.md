# coallo

Coallo is a way of describe and visualize softwares.
You can use coallo to describe green-fieldy, or old projects, however the last one may be harder since 
coallo is for going into details step by step, and a less detailed model may feel (and will be) useless.

**TODO: Detailed description of goals and usecases here**

Coallo uses md elements as it's main syntax with some addition.

If your .coallo file is a valid md, it does not mean that it's also a valid coallo. 

The next few lines (between horizontal lines) will be a demonstration of how to use coallo:
(Remommended switching to raw text mode)
---

### Types_are_3rd_headings
Types are exists only to restrict what methods can return.
You are not restricted to use types, but it helps coallo to find bugs,
and types are helpful additional information on the result graph. 
(Appears on edges.)


Every md element considered as comments, except **2nd and 3rd headers, unordered lists(including asterisk and hyphen), links.**

### String
Now a String type is exists!

### Number
Numbers are great, but what if you want more specific?

### Int extens Number
The hairy old guys calls this inheritance.
The only effect is that a method which expect a Number, will be fine with Int, but not backwards.

cicles are the main building blocks:
## Circles_are_2nd_headers
 - method1
 - method2

Basically a list of methods executed one after another.
You should consider them as steps.

## Header2_without_list_items_is_more_like_a_method

One list item can looks like this:
```
 - method_name
```

You can specify return type:
```
 - method_name:String
```
or type**s**:
```
 - method_name:String,Int
```

Input parameter type/types, if you sure about this level of detail:
```
 - Int,String:method_name
```
If you specify the input types, than you should specify every other return type in the circle as well:

## Very_detailed_circle
 - some_method_returns_something:Int
 - nothing_here
 - Int:Some_method_waiting_for_integer

In this case, coallo will see that **some_method_returns_something** have a return type, 
and **some_method_waiting_for_integer** waits for Int, so it's FINE, BUT:

## Missing_details_raising_warning
 - some_method_returns_nothing
 - also_nothing_here
 - Int:Some_method_waiting_for_integer

In this case, coallo will raise warning, "Missing return value in circle"

## Missing_details_raises_warning
 - some_method_returns_nothing
 - also_nothing_here
 - Int:Some_method_waiting_for_integer
 - returns_int_but_too_late:Int

This also raises warning, order of methods matters!

You can also describe your methods/steps:
```
 - Int:method_name:String This description considered as comment.
```

## Int,String:predefined_method
In case you predefine your method(which is the recommended way)
Than you can't change your mind:

## Circle_with_wrong_method
 - returns_integer
 - returns_integer
 - Int,Int:predefined_method this raises warning, since we defined it with Int,String separately


## Circle_with_void
 - some_locally_defined_method:String
 - the_last_method:void the void means that nothing returns

**Sub-lists** are forbidden! But you can embedd lists:

## Circle_with_embedded_circle
 - some_casual_method
 - Circle_with_void

Circle and method names are identical in term of syntax:

## Return_typed_circle : Int
 - step
 - this_step_gives_the_return_values:Int without it, coallo raises warning "Missing return type Int"
 - another_step

For the name of a circle/method/type, the rules are:
A variable name must start with a letter or the underscore character
A variable name cannot start with a number
A variable name can only contain alpha-numeric characters and underscores (A-z, 0-9, and _ )
Variable names are case-sensitive (age, Age and AGE are three different variables)
(just like in most programming languages)

---