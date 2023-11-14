import boto3
from fastapi import FastAPI,File,UploadFile
import glob
from pydantic import BaseModel

app=FastAPI()
class UserOut(BaseModel):
    result: str

@app.post("/face",responses=UserOut)
async def face(file:UploadFile):
    name="1"
    content=await file.read()
    
    file_path = '/Users/sangwoo/Desktop/img_download/'

    # (추가) 타겟 폴더에서 jpg 파일의 경로들을 리스트로 저장
    list_images= glob.glob(file_path + '*.jpg')
    # AWS 계정 정보 설정
    access_key = 'AWS_ACCESS_KEY'  # 자신의 액세스 키로 대체해야 함
    secret_key = 'AWS_SECRET_KEY'  # 자신의 시크릿 키로 대체해야 함
    region_name = 'ap-northeast-2'     # 사용하려는 리전으로 대체해야 함

    # AWS Rekognition 클라이언트 생성
    client = boto3.client('rekognition', aws_access_key_id=access_key,aws_secret_access_key=secret_key, region_name=region_name)

    for i in list_images:
        with open(i, 'rb') as stored_photo_file:
            target_image_bytes = stored_photo_file.read()

        # 얼굴 비교
        response = client.compare_faces(SimilarityThreshold=80, SourceImage={'Bytes': content},TargetImage={'Bytes': target_image_bytes})

        # 결과 확인
        face_matches = response['FaceMatches']
        if face_matches:
            similarity = face_matches[0]['Similarity']
            if similarity >= 95:
                if(name == "1"):
                    name ="1번학생의 이름과 학번"
                    return {"result": name}
                elif(name == "2"):
                    name="2번학생의 이름과 학번"
                    return {"result": name}
                elif(name == "3"):
                    name="3번학생의 이름과 학번"
                    return {"result": name} # 얼굴이 일치하지 않는 경우
    return {"result": name}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app,host="0.0.0.0",port=8000)