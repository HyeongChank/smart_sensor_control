# N = int(input())
# result = []
# blink = ' '
# for i in range(1, N+1):
#     print(blink * (N-i) + '*' * ((2* i)-1) )

# for i in range(N, 0, -1):
#     print(blink * ((N-i)+1) + '*' * ((2*(i-1))-1))
    


text = input()
upper_text = text.upper()
text_list = list(upper_text)
result = {}
text_list_set = set(text_list)
for t in text_list:
    if t in result:
        result[t] += 1
    else:
        result[t] = 1
maxvalue = max(result.values())
maxkey = [key for key, value in result.items() if value == maxvalue]
if len(maxkey) >=2:
    print('?')
else:
    print(maxkey[0])
print(result)
print(result.get('A'))