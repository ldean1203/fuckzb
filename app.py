from flask import Flask, render_template, redirect, url_for, request
import xlrd
import sys
import os

def cal_sum(path):
    # path = sys.argv[1]
    # workbook = xlrd.open_workbook('/Users/Dean/Desktop/d.xlsx')
    workbook = xlrd.open_workbook(path)

    sheet2 = workbook.sheets()[0]

    start = 1
    end = 0
    start_date = 0
    nrows = sheet2.nrows
    name = sheet2.cell(1, 0).value
    first_date = xlrd.xldate_as_tuple(sheet2.cell(start , 1).value, 0)[0:2]

    l = []
    l2 = []
    all_cnt = 0
    for i in range(2, nrows):
        if xlrd.xldate_as_tuple(sheet2.cell(i , 1).value, 0)[0:2] != first_date[0:2]:
            end = i - 1
            l.append((start, end))
            start = i
            first_date = xlrd.xldate_as_tuple(sheet2.cell(start , 1).value, 0)[0:2]
        if i == nrows - 1:
            end = nrows - 1
            l.append((start, end))


    for i in l:
        cnt = 0
        for j in range(i[0], i[1] + 1):
            v6 = float(sheet2.cell(j, 6).value)
            v7 = float(sheet2.cell(j, 7).value)
            v8 = float(sheet2.cell(j, 8).value)

            if v7 == 0.0 and v6 != 0.0:
                if v6 >= 9:
                    cnt += v6 - 0.5
            elif v7 == 0.0 and v6 == 0.0:
                cnt += 0.0
            if v7 >= 9:
                cnt += v7  - 0.5
            else:
                cnt += v7
        all_cnt += round(cnt)
        l2.append((xlrd.xldate_as_tuple(sheet2.cell(i[0] , 1).value, 0)[0], xlrd.xldate_as_tuple(sheet2.cell(i[0] , 1).value, 0)[1], round(cnt)))

    return l2, all_cnt, name

app = Flask(__name__)

@app.route('/sum')
def sum_zb():
    size = os.path.getsize('1.xlsx')
    if size == 0:
        sumed_list = []
        all_cnt = 0
    else:
        try:
            sumed_list, all_cnt, uname = cal_sum('1.xlsx')
        except:
            open('1.xlsx', "wb").write(open('templates/1.xlsx', "rb").read())
            return render_template('error.html')
    return render_template('sum_zb.html', sumed_list = sumed_list, all_cnt = all_cnt, uname = uname)

@app.route('/sumed', methods=['POST'])
def sumed():
    file = request.files['file']
    if file.filename[-3:] == 'xls' or file.filename[-4:] == 'xlsx' :
        file.save(os.path.join('/app/3projects', '1.xlsx'))
    else:
        return render_template('error.html')
    return redirect(url_for('.sum_zb'))


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')

