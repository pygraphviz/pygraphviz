"""
Example showing use of unicode and UTF-8 encoding.
"""


import pygraphviz as pgv

# specify UTF-8 encoding (it is the default)
A = pgv.AGraph(encoding="UTF-8")

# nodes, attributes, etc can be strings or unicode
A.add_node(1, label="plain string")
A.add_node(2, label="unicode")

# you can enter unicode text as
hello = "Здравствуйте!"
A.add_node(3, label=hello)

# or using unicode code points
hello = "\u0417\u0434\u0440\u0430\u0432\u0441\u0442\u0432\u0443\u0439\u0442\u0435!"
A.add_node(hello)  # unicode node label

goodbye = "До свидания"
A.add_edge(1, hello, key=goodbye)

A.add_edge("שלום", hello)
# A.add_edge(1,3,hello="こんにちは / ｺﾝﾆﾁﾊ")
A.add_edge(1, "こんにちは")

print(A)  # print to screen
A.write("utf8.dot")  # write to simple.dot
