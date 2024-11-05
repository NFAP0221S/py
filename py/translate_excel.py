import pandas as pd
import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def translate_text(text, index):
    print(f"번역 중 (인덱스: {index})")
    if pd.isnull(text):
        return text  # 비어있는 셀은 그대로 유지
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",  # 모델을 GPT-4로 변경
            messages=[
                {"role": "user", "content": f"Translate the following text from Korean to English: {text}"}
            ]
        )
        return response.choices[0].message['content']
    except Exception as e:
        print(f"번역 오류: {e} - 입력 텍스트: {text}")
        return text  # 오류 발생 시 원래 텍스트 반환

def main(input_file, output_file):
    # 엑셀 파일 읽기
    df = pd.read_excel(input_file)

    # 데이터프레임의 모든 셀에 번역 적용
    for column in df.columns:
        for i, value in enumerate(df[column], start=1):
            df[column].iloc[i - 1] = translate_text(value, i)

    # 번역된 내용을 새로운 엑셀 파일로 저장
    df.to_excel(output_file, index=False)
    print("번역이 완료되어 새로운 엑셀 파일이 생성되었습니다:", output_file)

if __name__ == "__main__":
    # 입력 및 출력 파일 경로 설정
    input_file = '/Users/ihansol/Downloads/MSDS_AGM-77(수출용).xls'  # .xlsx 확장자로 변경
    output_file = '/Users/ihansol/Downloads/output_file.xlsx'  # .xlsx 확장자로 변경

    main(input_file, output_file)