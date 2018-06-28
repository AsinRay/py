# ! /usr/bin/pyton
# -*- coding: utf-8 -*-
format_str = "{0:{3}^10}\t{1:^10}\t{2:^10}"  # 3表示format中第三个字符串chr（12288），中文空格
print(format_str.format("学校", "省份", "num", chr(122)))


format_str = "{0:^10}\t{1:^10}\t{2:^10}"  # 3表示format中第三个字符串chr（12288），中文空格
print(format_str.format("学校", "省份", "num"))

print(100//3)
print(100/3)
print(10 % 100 == 0)