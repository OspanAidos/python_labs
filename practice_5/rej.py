#1
import re
text = "ac ab abb abbb"
pattern = r"ab*"
print(re.findall(pattern, text))


#2
import re
text='a ab abb abbb abbbb'
pattern=r'ab{2, 3}'
print(re.findall(pattern, text))


#3
import re
text = 'a_b under_score re_match'
pattern=r'[a-z]+_[a-z]+'
print(re.findall(pattern, text))


#4
import re
text = 'Asus Banana Apple'
pattern=r'[A-Z][a-z]+'
print(re.findall(pattern, text))


#5
import re
text='ababab abbbbb ababaabb'
pattern=r'a.*b'
print(re.findall(pattern, text))


#6
import re
text = 'a.com b_a a,b,c'
result=re.sub(r'[ ,.]', ':', text)
print(result)


#7
import re
text = 'snake_case_string'
result = re.sub(r'_([a-b])', lambda m: m.group(1).upper(), text)
print(result)


#8
import re
text = 'NiceTryDiddy'
result=re.findall(r'[A_Z][^A-Z]*', text)
print(result)


#9
import re
text = 'YeahICameInWithTheSause'
result=re.sub(r'?=[A-Z]', ' ', text)
print(result)


#10
import re
text = "camelCaseString"
result = re.sub(r"(?<!^)(?=[A-Z])", "_", text).lower()
print(result)