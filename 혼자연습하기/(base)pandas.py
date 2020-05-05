import pandas as pd
pd.set_option('display.max_rows',500)
pd.set_option('display.max_columns',500)
pd.set_option('display.width', 1000)


#1)
# array = pd.Series(['사과', '바나나', '당근'], index = ['a','b','c'])
# print(array)
# print(array['a'])

#2) dict자료를 Series로 바꾸기 -> Dataframe 만들기
word_dict = {
    'apple' : '사과',
    'banana' : '바나나',
    'carrot' : '당근'
}

frequency_dict = {
    'apple' : 3,
    'banana' : 5,
    'carrot' : 7
}

importance_dic = {
    'apple' : 3,
    'banana' : 2,
    'carrot' : 1
}

word = pd.Series(word_dict)
frequency = pd.Series(frequency_dict)
importance = pd.Series(importance_dic)

#Dataframe 만들기
summary = pd.DataFrame({
    'word' : word ,
    'frequency' : frequency,
    'importance' : importance
}
)

score = summary['frequency'] * summary['importance']
summary['score'] = score
print(summary)
# df_sample = pd.DataFrame([[4,2,3],[9,1,5]])
# print(df_sample)
