*Below is a list of all of some other helpful functions available within spark.*

All of the examples below assume you have the boilerplate from [the notebook setup](../#boilerplate) in your code

### Create a random float between 0 and 1

To generate a random float between 0 and 1 use:

```python
random()
```

**Example(s):**

*Printing a random value between 0-1*

```python hl_lines="5"
%%ignite

def setup():
    size(200, 200)
    print(random())
```

Results in:

![random demo](img/random.png)



### Create a random int

To generate a random integer between 0 and n (inclusive) use:

```python
randint(n)
```

**Parameters**

- n: (int) The highest value in the range

**Example(s):**

*Printing a random value between 0-10*

```python hl_lines="5"
%%ignite

def setup():
    size(200, 200)
    print(randint(10))
```

Results in:

![random demo](img/randint.png)

### Pick a random choice from a list

To pick a random choice from a list use:

```python
choice(l)
```

**Parameters**

- l: (list) The list to pick a value from

**Notes**
- This function also lets you pick a single letter from a string

**Example(s):**

*Displaying a random choice from the a shopping list*

```python hl_lines="6"
%%ignite

def setup():
    size(200, 200)
    shopping_list = ["eggs", "ham", "cheese", "onions"]
    random_choice = choice(shopping_list)
    text_size(32)
    text(random_choice, 100, 20)
```

Results in:

![choice demo](img/choice.png)

### Working with dates and times

**Note this is somewhat complicated to work with**

To pick a random choice from a list use:

```python
datetime()
```


**Example(s):**

*...*

```python hl_lines="6"
%%ignite

def setup():
    size(200, 200)
    shopping_list = ["eggs", "ham", "cheese", "onions"]
    ...
```

Results in:

![datetime demo](img/datetime.png)

