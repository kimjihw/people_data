import numpy as np
import matplotlib.pyplot as plt
import csv


# area : 입력받은 지역이름
# allsum : 총인구수
# sum_m : 남성인구수
# sum_f : 여성인구수
# foundName : 검색된 지역이름
# age : 입력 받은 나이 (Age는 연령별 인구수 출력메소드)

class population:

    def __init__(self, area):  # 입력받은 지역이름을 area로 받음
        self.area = area


    def Cal(self):  # 입력받은 지역의 인구수 추출 메소드
        infile = open('./gender.csv')
        data = csv.reader(infile)
        next(data)

        self.foundArea = ''
        self.man_array = []
        self.woman_array = []
        for row in data:
            if self.area in row[0]:
                self.man_array = np.array(row[3:104], dtype=int)
                self.woman_array = np.array(row[106:], dtype=int)
                self.foundArea = row[0]
                break

        if len(self.man_array) == 0 or len(self.woman_array) == 0:
            print("\n검색결과가 없습니다\n")
            self.allSum = -1
            self.allMan = -1
            self.allWoman = -1
        else:
            self.allSum = np.sum(self.man_array + self.woman_array)
            self.allMan = sum(self.man_array)
            self.allWoman = sum(self.woman_array)
            self.people_array = self.man_array + self.woman_array  # 그래프 만들때 사용하기위해 만들어놓은 리스트

        infile.close()

    def total(self):  # 총인구수 출력 메소드
        if self.allSum == -1:
            return

        print('{0}의 총인구수 : {1}'.format(self.foundArea, self.allSum))

    def gender(self):  # 남녀 인구수 출력 메소드
        if self.allMan == -1 or self.allWoman == -1:
            return
        print('{0}의 남성 인구수 : {1}\n{0}의 여성 인구수 : {2}'.format(self.foundArea, self.allMan, self.allWoman))

    def Age(self, age):  # 나이별 인구수 출력 메소드
        infile = open('gender.csv')
        data = csv.reader(infile)
        self.man = -1
        self.woman = -1
        self.foundArea = ''

        for row in data:
            if self.area in row[0]:
                self.foundArea = row[0]
                self.man = int(row[age + 3])
                self.woman = int(row[age + 106])
                break

        if self.man == -1 or self.woman == -1:
            print('\n검색되지 않았습니다.\n')
            return
        else:
            self.allSum = self.man + self.woman
        print('{0}지역의 {1}세 총 인구수 : {2}\n{0}지역의 {1}세 남성 인구수 : {3}\n{0}지역의 {1}세 여성 인구수 : {4}\n' \
              .format(self.foundArea, age, self.allSum, self.man, self.woman))

        infile.close()

    def gender_graph(self):
        age = []
        plt.rcParams['font.family'] = 'Malgun Gothic'
        plt.rcParams['font.size'] = 10
        plt.rcParams['figure.figsize'] = (12, 12)
        for i in range(101):
            age.append(i)
        plt.plot(age, self.man_array)
        plt.plot(age, self.woman_array)
        plt.xlabel('연령')
        plt.ylabel('인구 수')
        plt.title('검색한 지역')
        plt.legend(['Man', 'Woman'])
        plt.show()

    def gender_graph_man(self):

        x = np.round((self.people_array / self.allMan), 2) * 100
        y = np.round((self.people_array / self.allWoman), 2) * 100

        total = [sum(x), sum(y)]
        person = ['남자', '여자']

        plt.rcParams['font.family'] = 'Malgun Gothic'
        plt.rcParams['font.size'] = 10
        plt.rcParams['figure.figsize'] = (12, 12)

        color = ['#FF0000', '#86E57F', ]
        explode = [0.01, 0.0]

        plt.figure()
        plt.title(f' {self.area}의 성비')
        plt.pie(total, labels=person, colors=color, explode=explode, autopct='%0.2f%%',
                shadow=False, startangle=270, counterclock=False)

        plt.legend()
        plt.show()

    def gender_graph3(self, age):

        infile = open('gender.csv')
        data = csv.reader(infile)
        for row in data:
            if self.area in row[0]:
                self.foundArea = row[0]
                man = int(row[age + 3])
                woman = int(row[age + 106])

        total = man + woman

        x = ['man', 'woman']
        y = [np.round((man / total), 4), np.round((woman / total), 4)]

        # plt.rcParams['font.family'] = 'Malgun Gothic'
        # plt.rcParams['font.size'] = 10
        # plt.rcParams['figure.figsize'] = (10, 10)

        plt.bar(x, y, width=0.5, color = ['#D9418C', '#F2CB61'])

        for i, v in enumerate(x):
            plt.text(v, y[i], y[i],  # 좌표 (x축 = v, y축 = y[0] ..y[1], 표시 =y[0] ..y[1])
                     fontsize=9,
                     color='black',
                     horizontalalignment='center',
                     verticalalignment='bottom',
                     )
        # plt.title(f' {self.area}의 {age}세 남 여 비율')

        plt.show()

    @staticmethod
    def city_total():
        import math, re
        f = open('./population.csv', 'r', encoding='CP949')
        data = csv.reader(f)
        next(data)
        lst = []
        for i in data:
            lst.append(i)

        city = []
        value = []
        arr = []
        for i in range(len(lst) - 1):
            hdr = lst[i + 1][0]
            total = lst[0][1]
            cnt = lst[i + 1][1]

            arr.append(hdr)
            value.append(cnt)
            city.append(re.sub(r'\([^)]*\)', '', arr[i]).rstrip())

        total = str(total)
        total = total.replace(',', '')
        total = int(total)

        city_value = []
        for i in list(map(lambda x: int(x.replace(',', '')), value)):
            value = round(i / total, 2) * 100
            value = math.ceil(value)

            city_value.append(value)

        plt.rcParams['font.family'] = 'Malgun Gothic'
        plt.rcParams['font.size'] = 10
        plt.rcParams['figure.figsize'] = (12, 12)

        color = ['#FF0000', '#800000', '#FFFF00', '#808000', '#00FF00', '#008000', '#00FFFF', '#008080', '#E4F7BA',
                 '#86E57F', '#B5B2FF', '#D9418C', '#F2CB61', '#FAE0D4', '#F15F5F', '#00D8FF', '#FF5E00', '#D5D5D5',
                 '#C4B73B']  # 컬러 설정
        explode = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

        plt.figure()
        plt.title('국내 인구 비율')
        plt.pie(city_value, labels=city, colors=color, explode=explode,
                autopct='%0.1f%%', shadow=False, startangle=180)

        plt.legend()  # 범주 표시
        plt.show()

    def similar(self):

        if self.allSum == -1:
            return
        infile = open('age.csv','r')
        data = csv.reader(infile)
        min = 1
        myArea_pct = []

        for row in data:
            if self.area in row[0]:
                myArea_pct = np.array(row[3:], dtype=int)/int(row[1])
                self.area = row[0]
                break

        for row in data:
            cmpArea = np.array(row[3:], dtype=int)/int(row[1])
            gap = np.sum(abs(myArea_pct-cmpArea))
            if gap < min and self.area not in row[0]:
                min = gap
                foundArea = row[0]
                foundArea_pct = cmpArea
        print("입력한지역 : ", self.area)
        print("찾은 비슷한 지역 : ", foundArea)

        plt.rc('font', family = "Malgun Gothic")
        plt.plot(myArea_pct, label=self.area)
        plt.plot(foundArea_pct, label=foundArea)
        plt.legend()
        plt.show()
        infile.close()

    @staticmethod
    def growth():
        infile = open('year.csv')
        data = csv.reader(infile)

        dec_pop = []
        num1 = 2011
        num2 = 2011
        year = []
        plot_x = []

        while (True):
            out = int(input("1.인구 성장률 지역 검색 2.나가기\n"))

            if out == 1:
                print("-------------------------------------------인구 성장률-------------------------------------------\n")
                print("1.전국 2.서울특별시 3.부산광역시 4.대구광역시 5.인천광역시 6.광주광역시 7.대전광역시 8.울산광역시 9.세종특별시\n")
                print("10.경기도 11.강원도 12.충청복도 13.충청남도 14.전라북도 15.전라남도 16.경상북도 17.경상남도 18.제주특별자치도")
                print(
                    "-----------------------------------------------------------------------------------------------\n")
                area = input("찾는 지역을 입력하시오: ")

                for i in data:
                    if area in i[0]:
                        for j in range(1, len(i)):
                            i[j] = i[j].replace(',', '')
                        for k in range(1, 61, 6):
                            dec_pop.append(i[k])

                        for j in range(0, 9):
                            grow = (int(dec_pop[j + 1]) - int(dec_pop[j])) / int(dec_pop[j + 1]) * 100

                            year.append(num1)
                            plot_x.append(round(grow, 2))
                            num1 += 1

                        choice = int(input("1. 출력으로 보기 2. 그래프로 보기\n"))


                        if choice == 1:
                            for g in range(0, 9):
                                a = (int(dec_pop[g + 1]) - int(dec_pop[g])) / int(dec_pop[g + 1]) * 100
                                print("%s의 %d년 인구 성장률: %.2f %% " % (area, num2, a))
                                num2 += 1

                        elif choice == 2:
                            dec_pop.pop(0)
                            x = year

                            plt.rcParams['font.family'] = 'Malgun Gothic'
                            plt.rcParams['font.size'] = 10
                            plt.rcParams['figure.figsize'] = (10, 10)
                            plt.rcParams['axes.unicode_minus'] = False
                            plt.title("%s의 인구 성장률" % area)

                            plt.plot(x, plot_x)
                            for i, v in enumerate(x):
                                plt.text(v, plot_x[i], plot_x[i],  # 좌표 (x축 = v, y축 = y[0] ..y[1], 표시 =y[0] ..y[1])
                                         fontsize=9,
                                         color='black',  # 숫자 색
                                         horizontalalignment='center',
                                         verticalalignment='bottom',
                                         )
                            plt.show()

            elif out == 2:
                break

    @staticmethod
    def avg():
        global sex
        infile = open('gender.csv')
        data = csv.reader(infile)


        man = []  # 남자의 나이별 인구 수
        woman = []  # 여자의 나이별 인구 수
        man2 = []
        woman2 = []

        next(data)

        re = input("지역 이름 : ")  # 지역 이름 받고
        for i in data:  # 데이터를 i에 집어넣고
            if re in i[0]:  # 지역이름이 아니면 넘어가고 맞으면 출력하고
                for j in range(3, 104):  # 남자는 3부터 104까지가 0세부터 100세까지니까 그걸 j에다가 넣고
                    a = int(i[j]) * (j - 2)  # j에 넣은 데이터에다가 각각의 나이를 곱하고
                    man.append(a)  # man리스트에 a를 넣고
                    qw = int(i[j])  # qw에 총 인구 수 넣고
                    man2.append(qw)  # man2리스트에 총 인구 수 넣고
                m = sum(man)  # man을 sum으로 다 더하고
                m2 = sum(man2)  # man2도 다 더하고
                avg_man = round(m/m2, 2)# man2에서 man을 나눈다.    지역 총 인구 나이 평균 구하는 공식 : 총인구수 * 각각의 나

                for j in range(106, 207):
                    a = int(i[j]) * (j - 105)
                    woman.append(a)
                    er = int(i[j])
                    woman2.append(er)
                w = sum(woman)
                w2 = sum(woman2)
                avg_woman = round(w/w2, 2)

                sex = [avg_man, avg_woman]


        x = ['man', 'woman']

        plt.rcParams['font.family'] = 'Malgun Gothic'
        plt.rcParams['font.size'] = 10
        plt.rcParams['figure.figsize'] = (12, 12)
        plt.bar(x, sex, width=0.5, color=['#D5D5D5','#FF5E00'])

        for i, v in enumerate(x):
            plt.text(v, sex[i], sex[i],  # 좌표 (x축 = v, y축 = y[0] ..y[1], 표시 =y[0] ..y[1])
                     fontsize=9,
                     color='black',
                     horizontalalignment='center',
                     verticalalignment='bottom',
                     )
        plt.show()
        # 원하는 지역의 65세 이상인구가 몇프로인지

    @staticmethod
    def aging():
        infile = open("gender.csv")
        data = csv.reader(infile)
        next(data)
        foundArea = ''
        agingarea = []
        x = input('원하는 지역 : ')
        for row in data:
            if x in row[0]:
                foundArea = row[0]
                men_some = 0
                women_some = 0
                men_some2 = 0
                women_some2 = 0
                men_sum = 0
                women_sum = 0
                for i in range(68, 104):
                    men_some += int(row[i])

                for i in range(171, 207):
                    women_some += int(row[i])

                for i in range(3, 68):
                    men_some2 += int(row[i])

                for i in range(106, 171):
                    women_some2 += int(row[i])

                for i in range(68, 104):
                    men_sum += int(row[i])

                for i in range(171, 206):
                    women_sum += int(row[i])

                if((men_sum + women_sum)/ (int(row[1]) + int(row[105])))> 0.3:
                    agingarea.append(row[0])

                for i in range(68, 104):
                    men_sum += int(row[i])

                for i in range(171, 206):
                    women_sum += int(row[i])

                if((men_sum + women_sum)/(int(row[1]) + int(row[105]))) > 0.3:
                    agingarea.append(row[0])

        print(agingarea)

        result = (men_some + women_some) / (int(row[1]) + int(row[105]))
        result = result*100
        result2 = (men_some2 + women_some2) / (int(row[1]) + int(row[105]))
        result2 = result2*100

        per = [result, result2]
        age = ['65세 이상', '65세 미만']

        plt.rcParams['font.family'] = 'Malgun Gothic'
        plt.rcParams['font.size'] = 10
        plt.rcParams['figure.figsize'] = (12, 12)

        color = ['#D9418C', '#F2CB61']  # 컬러 설정
        explode = [0.07, 0.0]

        plt.figure()
        plt.title(f'{x}의 고령화 비율 및 고령화로 접어든 지역 {len(agingarea)}개')
        plt.pie(per, labels=age, colors=color, explode=explode,
                autopct='%0.1f%%', shadow=False, startangle=270)

        plt.legend()  # 범주 표시
        plt.show()
        # 원하는 지역의 65세 이상인구가 몇프로인지

    @staticmethod
    def household_():

        infile = open('./year.csv')
        data = csv.reader(infile)

        household = []  # 세대별 인구수를 리스트에 저장하기 위해 선언
        year = []  # 2010년도부터 2019년도 까지의 연도를 리스트로 받아 줄 빈 리스트
        exit = -1  # 아래 while문에서 입력받은 값이 배열에 없는 경우 다시 입력하라는 말은 출력하기 위해 선언

        while (True):
            show = int(input("0.나가기 1.지역검색 \n"))
            if show == 1:
                print("-------------------------------------------세대수 최대최소-------------------------------------------\n")
                print("전국 서울특별시 부산광역시 대구광역시 인천광역시 광주광역시 대전광역시 울산광역시 세종특별시\n")
                print("      경기도 강원도 충청복도 충청남도 전라북도 전라남도 경상북도 경상남도 제주특별시")
                print("-----------------------------------------------------------------------------------------------\n")
                area = input("찾는 지역을 입력하시오: ")

                for recv in data:
                    if area in recv[0]:  # 만약 지역이 존재한다면
                        exit = 1  # 입력한 값이 존재하면 위의 선언된 a 에서 1의 값을 뺴준다.
                        for k in range(3, 61, 6):
                            household.append(recv[k])  # 매 행마다 인덱스 3부터 61까지 6씩 건너뛰며 genlst로 값 추가
                        # print(genlst)   # 입력받은 지역이 존재하면 해당 지역의 세대당 인구 수 출력

                        for ye in range(2010, 2020):  # year라는 리스트에 2010년부터 2019년 까지를 넣어준다.
                            year.append(ye)

                        for b in range(0, 10):  # 인덱싱을 위해 0부터 9까지 돌려주고 연도와 연도별 세대당 인구 수를 매치 시켜준다.
                            household[b] = float(household[b])
                            print("%s 지역의 %s년도 세대당 인구 수는 %s명 입니다." % (area, year[b], household[b]))

                        x = np.arange(10)
                        yearg = [2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019]
                        values = (household)

                        plt.rcParams['font.family'] = 'Malgun Gothic'
                        plt.rcParams['font.size'] = 10
                        plt.rcParams['figure.figsize'] = (12, 12)
                        plt.bar(range(len(yearg)), values, color='g')
                        plt.xticks(x, yearg, rotation=30)
                        plt.xlabel('years')
                        plt.ylabel('population per household')
                        plt.title(f'{area}의 세대당 인구 수')
                        for i, v in enumerate(x):
                            plt.text(v, household[i], household[i],  # 좌표 (x축 = v, y축 = y[0]..y[1], 표시 = y[0]..y[1])
                                     fontsize=9,
                                     color='black',
                                     horizontalalignment='center',  # horizontalalignment (left, center, right)
                                     verticalalignment='bottom')  # verticalalignment (top, center, bottom)
                        plt.show()

                if exit == -1:  # 위의 선언되었던 a 가 if문을 돌지 않아 그대로 1인경우 아래와 같이 출력한다.
                    print("이런!! 검색결과가 없습니다!")
            elif show == 0:
                break
if __name__ == '__main__':

    while (True):
        print('\n1. 지역 총인구수  \n2. 지역 남녀인구수 \n3. 지역 나이대별 인구수\n4. 우리동네와 비슷한 지역 찾기\n5. 도시인구 비율 보기 \n6. 인구 성장률 '
              '\n7. 지역별 남녀 나이 평균 \n8. 고령화 지역 \n9. 세대당 인구 수')
        choice = int(input())
        if choice < 1 or choice > 9:
            continue

        elif choice == 1:
            receive = input('찾고 싶은 지역을 입력하세요 : ')
            p = population(receive)
            p.Cal()
            p.total()
            if p.allSum == -1:
                continue
            while (True):
                print('\n 1. 그래프로 보기 \n 2. 돌아가기')
                a = int(input())
                if a < 1 or a > 2:
                    continue
                elif a == 1:
                    p.gender_graph()
                else:
                    break

        elif choice == 2:
            receive = input('찾고 싶은 지역을 입력하세요 : ')
            p = population(receive)
            p.Cal()
            if p.allSum == -1:
                continue

            p.gender()
            while (True):
                print('\n 1. 그래프로 보기 \n 2. 돌아가기')
                a = int(input())
                if a < 1 or a > 2:
                    continue
                elif a == 1:
                    p.gender_graph_man()
                else:
                    break

            print('\n')

        elif choice == 3:
            receive = input('찾고 싶은 지역을 입력하세요 : ')
            p = population(receive)
            p.Cal()
            if p.allSum == -1:
                continue
            while (True):

                try:
                    age = int(input('찾고 싶은 나이을 입력하세요 : '))
                except ValueError:
                    print("숫자를 입력해주세요")
                    continue

                if age > 100 or age < 0:
                    print('0~100 숫자까지 검색가능합니다')
                    continue
                else:
                    break

            p.Age(age)
            while (True):
                print('\n 1. 그래프로 보기 \n 2. 돌아가기')
                a = int(input())
                if a < 1 or a > 2:
                    continue
                elif a == 1:
                    p.gender_graph3(age)
                else:
                    break



        elif choice == 4:
            receive = input('찾고 싶은 지역을 입력하세요 : ')
            p = population(receive)
            p.Cal()
            if p.allSum == -1:
                continue
            p.similar()

        elif choice == 5:
            population.city_total()

        elif choice == 6:
            population.growth()

        elif choice == 7:
            population.avg()

        elif choice == 8:
            population.aging()

        elif choice == 9:
            population.household_()
exit()