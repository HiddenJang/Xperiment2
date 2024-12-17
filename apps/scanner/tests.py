def exx():
    string_1 = 'lineEdit_loginLeon'
    return string_1


match 'login' in :
    case exx():
        print('YES!')
    case _:
        print('NO!')
