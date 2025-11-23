### repo 의 목적

- 개인적으로 머신러닝 전체에 대해서 공부하여 정리하는 repo 가 필요하기도 했고
- 스스로 공부한 내용들을 정리하고 싶기도 했고
- 친구들을 알려줄 때 필요한 내용들을 정리 할 목적도 있었음.


### 사용 언어 및 환경
- python3.12 + pytorch
- 기타 사항은 poetry 를 이용해서 관리 할 예정.
- 필자 gpu 는 RTX4080을 사용하고 있으나, 최대한 작은 모델을 사용해서 실습 할 것이라 VRam 6GB 이내에서 모두 해결 할 것.


### 데이터
- 대부분 AIHub 혹은 huggingface 에 공개된 데이터만 사용 할 것 입니다.
- AIHub Data의 경우 반출 할 수 없기 때문에, 사용 할 경우 어떤 데이터셋을 사용했는지 명시적으로 기록만 해 두겠습니다. (직접 받아야 함)
- huggingface data 역시 해당 repo에 포함시키지는 않고, 어떤 데이터를 사용했는지 기록 해 두겠습니다.
- 외부 데이터를 사용하여, 영리목적의 프로그램 개발 / 서비스 시 법률적 문제가 있을 수 있으며, 각 사용 데이터의 라이센스를 저는 학습용으로 가능 한 데이터를 사용할 것이기 때문에, 영리 목적으로 사용시에는 다른 검토가 필요 할 수 있습니다.


### 해당 강의에서 다루는 것
- python programming
- Machine Learning 지식
- git 을 이용한 협업 (타 repo 에서 진행 예정)


### 목차
 - week_1
   - AIHub 와 HuggingFace 소개
   - Data 구조 개론
   - git 간단 설명 (진짜 당장 필요한 것만)
   - ML의 역사 (간략하게)
 
 - week_2
   - git clone 하는 방법
   - shell 이란?
   - python 가상 환경
   - vscode 와 jupyter
   - python code, 자료구조 시각화
   - Support Vector Machine
   - Random Forest

 - week_3
   - 머신러닝이란 무엇인가?
   - Neural Network
   - Back Propagation 설명
   - Activation과 Loss 함수
   - Pytorch 기초
   - Auto Encoder 와 Variational Auto Encoder
   - Convolution Neural Network
   - 강화학습이란 무엇인가
   - GAN

- week_4
  - sequence to sequence 란 무엇인가?
  - Text Embedding
  - n-gram modeling
  - LSTM과 그 친척들

- week_5
  - Transformer
  - Diffusion

- week_6
  - VIT (Vision Transfromer)
  - Text_Embedding Diffusion

### 이후 논문 서치 및 구현