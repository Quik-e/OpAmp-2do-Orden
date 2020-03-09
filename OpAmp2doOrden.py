# By Quique Cametti

import numpy as np
import matplotlib.pyplot as plt

fmax=80e6 #Frecuencia máxima del plot
i=1
while 1:
    print("-----------------------------------------------------")
    print("***Circuito {}***".format(i))
    
    # Ingreso de datos
    f1=float(input("Ingrese frecuencia del primer polo (kHz): "))
    f2=float(input("Ingrese frecuencia del segundo polo (kHz): "))
    To=float(input("Ingrese |To| (no en dB): "))
    Bn=float(input("Ingrese Bn (no en dB): "))
    Invs=input("Invierte señal?(S/N) ")
    while Invs.upper()!="S" and Invs.upper()!="N":
        print("Ingrese respuesta correcta")
        Invs=input("Invierte señal?(S/N)")
    if Invs.upper()!="S":
        Inv=1
    if Invs.upper()!="N":
        Inv=-1
    # Cálculo de variables
    fo=np.sqrt(f1*f2*(1+To)) # kHz
    FdA=(f1+f2)/(2*fo)
    fc=fo*np.sqrt(np.sqrt(4*FdA**4+1)-2*FdA**2) # kHz
    fcorte=fo*np.sqrt(1-2*FdA**2+np.sqrt((2*FdA**2-1)**2+1))
    PM=np.rad2deg(np.arctan(np.sqrt(4*FdA**2/(np.sqrt(4*FdA**4+1)-2*FdA**2))))
    if(FdA<1/np.sqrt(2)):
        fp=fo*np.sqrt(1-2*(FdA**2)) # kHz
        Mpf=1/(2*FdA*np.sqrt(1-FdA**2)) # Por unidad
        tp=1000/(2*fo*np.sqrt(1-FdA**2))
        Mpt=100*np.exp(-np.pi*FdA/(1-FdA**2))
        Tr=2000000/fc # ns
    else:
        Tr=3500000/fc # ns
    Q=1/(2*FdA)

    # Resultados en pantalla
    print("\n***Resultados {}***".format(i))  
    print("Frecuencia de oscilación (fo): {:.3f} kHz".format(fo))
    print("Factor de amortiguamiento (E): {:.3f}".format(FdA))
    print("Frecuencia de cruce (fc): {:.3f} kHz".format(fc))
    print("Frecuencia de corte (fcorte): {:.3f} kHz".format(fcorte))
    print("Margen de fase (PM): {:.3f}°".format(PM))
    if(FdA<1/np.sqrt(2)):
        print("Frecuencia de pico (fp): {:.3f} kHz".format(fp))
        print("Sobrepico de la respuesta en frecuencia (Mpf): {:.3f}".format(Mpf))
        print("Tiempo de pico (tp): {:.3f} us".format(tp))
        print("Sobrepico de la respuesta en tiempo (Mpt): {:.3f}%".format(Mpt))
    else:
        print("No hay sobrepico")
    print("Tiempo de crecimiento (Tr): {:.3f} ns".format(Tr))
    print("Factor Q: {:.3f}".format(Q))
    f=np.concatenate((np.arange(0,10,0.01).astype(float),np.arange(10,100,0.1).astype(float),np.arange(100,1000,1).astype(float),np.arange(1000,10000,10).astype(float),np.arange(10000,100000,100).astype(float),np.arange(100000,1000000,1000).astype(float),np.arange(1000000,fmax,10000).astype(float))) # Saltos del 1% del valor minimo de cada range para tener como máximo 1% de error en las frecuencias
    T=To/((1+1j*f/(f1*1000))*(1+1j*f/(f2*1000)));TdB=20*np.log10(np.abs(T));argT=np.angle(-T,True)-360 # s=jw  f1 y f2 estaban en kHz
    PE=T/(Bn*(T+1));PEdB=20*np.log10(np.abs(PE));
    if Inv==1:
        argPE=np.angle(PE*Inv,True)
    else:
        argPE=np.angle(PE*Inv,True)-360
    #Plot Bode
    #Amplitud Ganancia de Lazo
    plt.subplot(2,2,1)
    plt.plot(f,TdB)
    plt.xscale("log")
    plt.title("|T(f)|dB")
    plt.xlabel("f(log)")
    plt.axvline(f1*1000,color='r',ls='--');plt.axvline(f2*1000,color='navy',ls='--');plt.axvline(fc*1000,color='gold',ls='--')
    if f1<1:
        plt.text(f1*1000,20*np.log10(To)," f1={:.2f}Hz".format(f1*1000))
    if f1>=1 and f1<1000:
        plt.text(f1*1000,20*np.log10(To)," f1={:.2f}kHz".format(f1))
    if f1>=1000:
        plt.text(f1*1000,20*np.log10(To)," f1={:.2f}MHz".format(f1/1000))
    if f2<1:
        plt.text(f2*1000,20*np.log10(To)-10," f2={:.2f}Hz".format(f2*1000))
    if f2>=1 and f2<1000:
        plt.text(f2*1000,20*np.log10(To)-10," f2={:.2f}kHz".format(f2))
    if f2>=1000:
        plt.text(f2*1000,20*np.log10(To)-10," f2={:.2f}MHz".format(f2/1000))
    if fc<1:
        plt.text(fc*1000,0," fc={:.2f}Hz".format(fc*1000))
    if fc>=1 and fc<1000:
        plt.text(fc*1000,0," fc={:.2f}kHz".format(fc))
    if fc>=1000:
        plt.text(fc*1000,0," fc={:.2f}MHz".format(fc/1000))
    plt.grid()
    #Fase Ganancia de Lazo
    plt.subplot(2,2,3)
    plt.plot(f,argT)
    plt.xscale("log")
    plt.title("Fase T(f)")
    plt.xlabel("f(log)")
    plt.axvline(f1*1000,color='r',ls='--');plt.axvline(f1*100,color='r',ls='--');plt.axvline(f1*10000,color='r',ls='--')
    plt.axvline(f2*1000,color='navy',ls='--');plt.axvline(f2*100,color='navy',ls='--');plt.axvline(f2*10000,color='navy',ls='--')
    plt.axvline(fc*1000,color='gold',ls='--')
    plt.axhline(PM-360,color='gold',ls='--')
    plt.text(fc*1000,PM-360+5," PM={:.2f}°".format(PM))
    plt.grid()
    plt.ylim((-362,-178))
    #Amplitud Parámetro Estabilizado
    plt.subplot(2,2,2)
    plt.plot(f,PEdB)
    plt.xscale("log")
    plt.title("|PE(f)|dB")
    plt.xlabel("f(log)")
    if(FdA<1/np.sqrt(2)):
        plt.axvline(fp*1e3,color='navy',ls='--')
        if fp<1:
            plt.text(fp*1e3,20*np.log10(1/Bn)-10," fpico={:.2f}Hz".format(fp*1e3))
        if fp>=1 and fp<1e3:
            plt.text(fp*1e3,20*np.log10(1/Bn)-10," fpico={:.2f}kHz".format(fp))
        if fp>=1e3:
            plt.text(fp*1e3,20*np.log10(1/Bn)-10," fpico={:.2f}MHz".format(fp/1e3))
        
    plt.axvline(fcorte*1e3,color='r',ls='--')
    if fcorte<1:
        plt.text(fcorte*1e3,20*np.log10(1/Bn)-15," fcorte={:.2f}Hz".format(fcorte*1e3))
    if fcorte>=1 and fcorte<1e3:
        plt.text(fcorte*1e3,20*np.log10(1/Bn)-15," fcorte={:.2f}kHz".format(fcorte))
    if fcorte>=1e3:
        plt.text(fcorte*1e3,20*np.log10(1/Bn)-15," fcorte={:.2f}MHz".format(fcorte/1e3))
    plt.axvline(fo*1e3,color='r',ls='--')
    if fo<1:
        plt.text(fo*1e3,20*np.log10(1/Bn)-20," fo={:.2f}Hz".format(fo*1e3))
    if fo>=1 and fo<1e3:
        plt.text(fo*1e3,20*np.log10(1/Bn)-20," fo={:.2f}kHz".format(fo))
    if fo>=1e3:
        plt.text(fo*1e3,20*np.log10(1/Bn)-20," fo={:.2f}MHz".format(fo/1e3))
    plt.axvline(f1*1000,color='orange',ls='--');plt.axvline(f2*1000,color='orange',ls='--')
    if f1<1:
        plt.text(f1*1000,20*np.log10(1/Bn)," f1={:.2f}Hz".format(f1*1000))
    if f1>=1 and f1<1000:
        plt.text(f1*1000,20*np.log10(1/Bn)," f1={:.2f}kHz".format(f1))
    if f1>=1000:
        plt.text(f1*1000,20*np.log10(1/Bn)," f1={:.2f}MHz".format(f1/1000))
    if f2<1:
        plt.text(f2*1000,20*np.log10(1/Bn)-5," f2={:.2f}Hz".format(f2*1000))
    if f2>=1 and f2<1000:
        plt.text(f2*1000,20*np.log10(1/Bn)-5," f2={:.2f}kHz".format(f2))
    if f2>=1000:
        plt.text(f2*1000,20*np.log10(1/Bn)-5," f2={:.2f}MHz".format(f2/1000))
    plt.grid()
    #Fase Parámetro Estabilizado
    plt.subplot(2,2,4)
    plt.plot(f,argPE)
    plt.xscale("log")
    plt.title("Fase PE")
    plt.xlabel("f(log)")
    if Inv==-11:
        plt.ylim((-362,-178))
    if Inv==1:
        plt.ylim((-182,2))
    plt.axvline(fo*100,color='r',ls='--');plt.axvline(fo*1000,color='r',ls='--');plt.axvline(fo*10000,color='r',ls='--')
    plt.grid()
    plt.show()
    # for x in range(len(f)):
    #     if PEdB[x]<PEdB[0]-2.9 and PEdB[x]>PEdB[0]-3.1:
    #         print(f[x],PEdB[0]-PEdB[x])
    i+=1