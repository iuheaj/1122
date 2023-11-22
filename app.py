from flask import Flask, render_template
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from io import BytesIO
import base64

app = Flask(__name__)

@app.route("/")
def home():
    # CSV 파일 로드
    csv_file_path = r"C:\Github\1122\cox-violent-parsed_filt_usable.csv"
    data = pd.read_csv(csv_file_path)

    # 데이터 분석 및 시각화
    # 성별과 폭력적인 재범 발생 여부(is_violent_recid) 사이의 상관관계 분석
    gender_violent_recid_corr = data.groupby('sex')['is_violent_recid'].mean()

    # 인종과 폭력적인 재범 발생 여부(is_violent_recid) 사이의 상관관계 분석
    race_violent_recid_corr = data.groupby('race')['is_violent_recid'].mean()

    # 그래프 그리기
    plt.figure(figsize=(12, 6))

    # 성별에 대한 그래프
    plt.subplot(2, 1, 1)
    sns.barplot(x=gender_violent_recid_corr.index, y=gender_violent_recid_corr.values)
    plt.title('Correlation between Gender and Violent Recidivism')
    plt.xlabel('Gender')
    plt.ylabel('Mean Violent Recidivism')

    # 인종에 대한 그래프
    plt.subplot(2, 1, 2)
    sns.barplot(x=race_violent_recid_corr.index, y=race_violent_recid_corr.values)
    plt.title('Correlation between Race and Violent Recidivism')
    plt.xlabel('Race')
    plt.ylabel('Mean Violent Recidivism')

    # 그래프를 이미지로 변환하여 HTML로 전달
    img_buf = BytesIO()
    plt.savefig(img_buf, format='png')
    img_buf.seek(0)
    img_data = base64.b64encode(img_buf.read()).decode('utf-8')

    return render_template("index.html", img_data=img_data)

if __name__ == "__main__":
    app.run(debug=True)
