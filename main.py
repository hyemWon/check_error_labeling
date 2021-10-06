

import os
import shutil


class Preoprocessing:

    def __init__(self, datafile, metaPath):
        self.dir_current = os.getcwd()
        self.dir_name = datafile  # 현재 폴더에서 dataset 저장위치
        self.meta_path = metaPath
        self.meta_path_list = []


    def create_file_list(self):
        path_dataset = os.path.join(self.dir_current, self.dir_name)
        temp = []
        try:
            listfile = os.listdir(path_dataset)
            with open(self.meta_path, 'w') as f:
                for filename in listfile:
                    if filename.endswith(".txt"):
                        path = os.path.join(path_dataset, filename)
                        temp.append(path)
                        f.write(path + '\n')
            self.meta_path_list = temp
        except (FileNotFoundError) as e:
            print(f'에러: {path_dataset} 지정된 파일 경로를 찾을 수 없습니다.')


    # 4 클래스 삭제
    def remove_class(self, num):
        for path in self.meta_path_list:
            with open(path, 'r+') as f:
                new_f = f.readlines()
                f.seek(0)
                for line in new_f:
                    class_num = line.split()[0].strip()
                    if class_num != num:
                        f.write(line)
                f.truncate()


    # 클래스 개수
    def count_class(self):
        result = dict()
        for path in self.meta_path_list:
            with open(path, 'r') as f:
                for line in f:
                    obj = line.split()
                    obj[0] = obj[0].strip()
                    # 카운트할 클래스가 없으면 생성하고 1로 초기화
                    if obj[0] not in result:
                        result[obj[0]] = 1
                    else:
                        result[obj[0]] += 1
        return result


    # 좌표값 벗어나면 다른 폴더에 보관
    def check_coordinate(self, errorfile, width, height):
        for path in self.meta_path_list:
            with open(path, 'r') as f:
                for line in f:
                    _, x,y,w,h = line.split()

                    x = width * float(x)
                    y = height * float(y)
                    w = width * float(w)
                    h = height * float(h)

                    xmin, ymin = x-w/2, y-h/2
                    xmax, ymax = x+w/2, y+h/2

                    if xmin<0 or ymin<0 or xmax>720 or ymax>480:
                        try:
                            from_ = path
                            to_ = os.path.join(self.dir_current, errorfile)

                            shutil.move(from_, to_)
                            shutil.move(from_[:-3]+'jpg', to_)
                        except:
                            print('파일을 옮기지 못하였습니다.')






if __name__ == '__main__':

    dir_name = 'dataset'  # 현재 폴더에서 dataset 저장위치
    width, height = 720, 480

    data = Preoprocessing(dir_name, './list .txt')


    while True:
        print('-'*20 + ' Menu ' + '-'*20)
        print("""
        1. 메타데이터 경로 파일 생성
        2. 각 클래스 개수 출력
        3. 클래스 삭제
        4. 좌표 오류 파일 이동
        5. 프로그램 종료
        """)

        menu = ['1', '2', '3', '4', '5']
        menuNum = input('실행번호 입력: ').strip()

        if menuNum in menu:
            if menuNum == "1":
                data.create_file_list()
                print('업로드 되었습니다.')
            elif menuNum == "2":
                count = data.count_class()
                print(count)
            elif menuNum == "3":
                remove_class_num = input('삭제 클래스 번호 입력: ').strip()
                data.remove_class(remove_class_num)
                data.create_file_list()
                print("삭제되었습니다.")
            elif menuNum == "4":
                data.check_coordinate('dataset_error', width, height)
                data.create_file_list()
                print("좌표 오류 파일이 이동하였습니다.")
            elif menuNum == "5":
                print("프로그램 종료")
                break
        else:
            print('올바른 번호를 입력해주세요.')
