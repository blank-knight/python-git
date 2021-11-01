#encoding:utf-8
#括号匹配问题
import sys
sys.path.append('/home/zhaowentao/桌面/python_program/和鲸社区/data_structure/Stack_and_queue/')
import Sequential_stack
stack = Sequential_stack.sequential_stack()
print("Please input bracket")
left_brac = '{[('
right_brac = '}])'
bracket = input()
for i in range(len(bracket)-1,-1,-1):
        #为左括号时且不为空栈时，将top元素出栈，并判断出栈的元素索引在left_brac的
        #位置和right_brac右括号位置是否匹配，如果不匹配，则匹配错误
        if bracket[i] in left_brac and stack != []:
            if left_brac.find(bracket[i]) == right_brac.find(stack.pop()):
                continue
            else:
                print("匹配错误")
                break
        #为右括号或者空栈，直接入栈
        else:
            stack.push(bracket[i])
            
if stack.jug_empty() == 0:
    print("匹配正确")
