arrCosSimilar=[]
similarity_threshold=0.33 # 임시 변수 , 향후 프로젝트정보에서 읽어서 처리 

def gen_attention_mask(userQuery, sentence2):
####### 텍스트 유사도 측정 ######
    from sklearn.feature_extraction.text import TfidfVectorizer
    sentences = (userQuery,
            sentence2)
    tfidf_vectorizer = TfidfVectorizer()
     # 문장 벡터화 하기(사전 만들기)
    tfidf_matrix = tfidf_vectorizer.fit_transform(sentences)

    ### 코사인 유사도 ###
    from sklearn.metrics.pairwise import cosine_similarity
    # 첫 번째와 두 번째 문장 비교
    cos_similar = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
    #print("코사인 유사도 측정")
    # print(cos_similar)
    return cos_similar            
print("------1------")
 
import re
from konlpy.tag import Okt
t = Okt()
  
# chatbot_data2 : 인텐트 , userQuery:챗봇 질의
def makeCosSimilarArr(chatbot_data2, userQuery,  containNounYn):
    # nounsFromSentence = t.nouns(userQuery)
    # print("nounsFromSentence: ", userQuery, nounsFromSentence )    
    # varCosSimilar=[]

    #  프로젝트 내 인텐트내용(질문) , 필수엔티티, 제외
    for intent_id, question_seq, strSentence, strRequiredEntity, strExclusiveEntity in chatbot_data2 :
        containKeywordYnAll=True
        containKeywordYn=False      
        containStopwordYn=False         


        print("   "   )          
        print("for intent_id, question_seq, strSentence, strRequiredEntity, strExclusiveEntity" , intent_id, question_seq,strSentence, strRequiredEntity, strExclusiveEntity   )          

        #1 불용어 공통

        for strStopKeyword in re.split(',', strExclusiveEntity):
            stopYn = strStopKeyword in userQuery        # 문장내에 불용어가 포함되어 있으면 stopYn에 True, 없으면 False
            # print("-----1------ -0  stopYn and strStopKeyword !=", ":" , stopYn, ":" ,strStopKeyword , ":"  )                              
            if stopYn==True and strStopKeyword !="":
                print("-----1------ -1 if stopYn and strStopKeyword !=", stopYn, strStopKeyword   )          
                print("불용어: ", strStopKeyword, userQuery, stopYn)
                containStopwordYn=True


 

        print("-----1------ -1-1 stopYn, containStopwordYn", ":" , stopYn, ":" ,containStopwordYn , ":"  )                  

        #2 검색키워드 / 불용어
        if containNounYn != "Y" and containStopwordYn == False :
            print("-----1------ -2 if containNounYn !=", containNounYn )                        
            for strKeyword in re.split(',', strRequiredEntity):
                findYn = strKeyword in userQuery
                print("-----1------ -2-1 strRequiredEntity, strKeyword, findYn, strKeyword", ":" , strRequiredEntity , ":" , strKeyword,  ":" , findYn, ":" ,strKeyword , ":"  )                  
                if (findYn==True and strKeyword !="")  :
                    print("검색어 strKeyword strSentence findYn: ", strKeyword, ":" , strSentence, findYn)
                    containKeywordYn=True
                else :
                    containKeywordYn=False
                    containKeywordYnAll=False
                    print("검색어X strKeyword strSentence findYn: ", strKeyword, ":" , strSentence, findYn)

            print("-----1------ -2-2 containKeywordYn, containKeywordYnAll", ":" , containKeywordYn, ":" ,containKeywordYnAll , ":"  )                  


            # 키워드가 없거나 키워드가 포함된 문장이거나 불용어 미포함 문장일때 유사문서 대상에 들어감 
            if (containKeywordYnAll==True or strRequiredEntity=="") and containStopwordYn == False : 
                print("-----1------ -3 if containKeywordYnAll:", containKeywordYnAll )                                        
                sentence2=strSentence
                Intcos_similar = gen_attention_mask(userQuery, sentence2)
                print("-----1------ -3 intent_id question_seq sentence2 Intcos_similar " ,intent_id, question_seq, sentence2 , Intcos_similar)
                if (float(similarity_threshold) <= float(Intcos_similar) ) :

                    morphFromSentence = t.morphs(strSentence)

                    varCosSimilar=[]
                    varCosSimilar.append(intent_id)
                    varCosSimilar.append(question_seq)                                
                    varCosSimilar.append(sentence2)
                    varCosSimilar.append(Intcos_similar)
                    varCosSimilar.append(morphFromSentence)                
                    arrCosSimilar.append(varCosSimilar)

        #3 검색키워드 / 불용어               
        elif containNounYn == "Y" and containStopwordYn == False :
            containKeywordYn=False
            strNounAppend = ""


            for strNoun in nounsFromSentence :
                findYn = strNoun in strSentence
                #print(strNoun, findYn, strSentence)
                if findYn :
                    containKeywordYn=True
                else:
                    containKeywordYn=False
                    containKeywordYnAll=False

            # 키워드가 없거나 키워드가 포함된 문장이거나 불용어 미포함 문장일때 유사문서 대상에 들어감 
            if (containKeywordYnAll==True ) and containStopwordYn == False : 
                sentence2=strSentence
                Intcos_similar = gen_attention_mask(userQuery, sentence2)
                print("-----1------ -4 containKeywordYnAll==True", containKeywordYnAll )                                                        
                print("-----1------ -4 intent_id question_seq sentence2 Intcos_similar " ,intent_id, question_seq, sentence2 , Intcos_similar)
                if (float(similarity_threshold) <= float(Intcos_similar) ) :

                    morphFromSentence = t.morphs(strSentence)

                    varCosSimilar=[]
                    varCosSimilar.append(intent_id)
                    varCosSimilar.append(question_seq)                                
                    varCosSimilar.append(sentence2)
                    varCosSimilar.append(Intcos_similar)
                    varCosSimilar.append(morphFromSentence)                
                    arrCosSimilar.append(varCosSimilar)            

    # print(arrCosSimilar)    




    
print("-----2------") 
 

def main_test():
#if __name__ == '__main__':
    chatbot_data = [
                    '나 오늘 30분 늦게 가'
                    ,'내 근무시간 보여줘 '
                    , '오빠 결혼하는데 휴가 낼래요'
                    ,'경조사 지원금 신청어디서하나요?'
                ]

    chatbot_data2 = [
                    [1, 1, '나 오늘 30분 늦게 가' ],
                    [1, 2, '나 오늘 30분 늦게 가요' ],
                    [2, 1, '내 근무시간 보여줘' ],
                    [2, 2, '내 근무시간 보여줘요' ],
                    [3, 1, '오빠 결혼하는데 휴가 낼래요' ],
                    [3, 2, '오빠 결혼하는데 휴가 낼래' ],
                    [3, 3, '오빠 결혼하는데 휴가 내고싶어요' ],
                    [4, 1, '경조사 지원금 신청어디서하나요?' ],
                    [4, 2, '경조사 지원금 신청어디서해요?' ]                                                                                                                                            
                ]


    #순수 유사문서 조회
    rrCosSimilar=[] ; # arrCosSimilar=[]
    userQuery="내 근무시간 보여주세요"
    strFindKeyword = "" ; strStopKeyword="" ; containNounYn= "N" ; #  args['nounMatchingYn']
    makeCosSimilarArr(chatbot_data2, userQuery, strFindKeyword , strStopKeyword, containNounYn)   # simular_biz.


    result_data={} ; result_data['query'] = [] ; result_data['result'] = [] ; 
    arrCosSimilar.sort(key = lambda x:x[3] , reverse=True)          # # simular_biz.
    for intent_id, question_seq, strA1, strA2, strA3 in arrCosSimilar :       # # simular_biz.
        print(intent_id, question_seq, strA1, strA2, strA3)
        strA2Rounded=round(strA2[0][0], 2)
        result_data['result'].append({
            '내용' : strA1, 
            '형태소분석' : strA3,         
            '유사도' : strA2Rounded     
            })            
    print("result_data: ", result_data)     