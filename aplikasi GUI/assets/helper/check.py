def check_true(salat, gerak_now, rakaat_now, runtutan, gerak_curr):
    rakaat_dict = {
        'Shubuh' : 2,
        'Dzuhur' : 4,
        'Ashar' : 4,
        'Maghrib' : 3,
        'Isya' : 4,
        'Tidak Waktunya' : 0
    }

    rakaat_ganjil = ["berdiri", "ruku", "berdiri", "sujud", "duduk", "sujud", "berdiri"]
    rakaat_genap = ["berdiri", "ruku", "berdiri", "sujud", "duduk", "sujud", "duduk", "berdiri"]
    rakaat_akhir = ["berdiri", "ruku", "berdiri", "sujud", "duduk", "sujud", "duduk"]

    rukun_salat = {
        0 : [],
        2 : [rakaat_ganjil, rakaat_akhir],
        3 : [rakaat_ganjil, rakaat_genap, rakaat_akhir],
        4 : [rakaat_ganjil, rakaat_genap, rakaat_ganjil, rakaat_akhir]
    }

    rukun_dict = {
        0 : [0],
        2 : [1, 2],
        3 : [1, 2, 3],
        4 : [1, 2, 1, 3]
    }
    
    cetak = False
    cetak2 = False
    kebenaran = True
    gerak_next = ""
    
    if len(runtutan) == 0:
        gerak_curr = ""

    rukun = rukun_dict.get(rakaat_dict.get(salat))[rakaat_now]
    
    if gerak_now != gerak_curr:
        rukun_now = rukun_salat.get(rakaat_dict.get(salat))
        gerak_next = rukun_now[rakaat_now][len(runtutan)]
        
        if gerak_now == gerak_next:
            runtutan.append(gerak_now)
            
            print(runtutan)
            cetak = True
            
            gerak_curr = gerak_now

            if len(runtutan) >= len(rukun_now[rakaat_now]):
                rakaat_now += 1
                cetak2 = True
                runtutan = []

            gerak_next = rukun_now[rakaat_now][len(runtutan)]
        else:
            kebenaran = False

    return rakaat_now, runtutan, kebenaran, gerak_curr, gerak_next, cetak, cetak2, rukun