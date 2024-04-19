#from nltk.tokenize import word_tokenize
import openaiTest

openaiTest.api_key = "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"
answer = openaiTest.completions.create(
    model="gpt-3.5-turbo-instruct",
    prompt="Say this is a test",
    max_tokens=7,
    temperature=0
)
print(answer)


# sentence = "hey mimi what is the date today"

# output = word_tokenize(sentence)
# print(output)

#opeinai appkey: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