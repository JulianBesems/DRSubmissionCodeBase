import time, random, datetime, pygame
from threading import Thread
from geometries import Point, Line, Face, Box
from shelves import *
from shelvingClusters import *
from shelvingUnits import *
from books import Book, BookCollection
from geometries import *

levels = 6

def convert(β, η, σ, ρ, λ, π, ψ, μ, ω, α, δ):
    PC = ρ + λ + π
    PX = β + η + σ + ρ + λ + π
    BBX = PX
    BBMAX = int(1/11 * PX) + 2*λ + π
    BEX = BBX
    BEMAX = int(1/11 * PX) + 2*ρ + π
    SC = ρ + 2*π
    S = 2*β + 2*η + 3*σ + 6*λ + 4*π
    EB = σ + 2*λ + (β + σ + ρ + λ + π)
    EC = β + η + ρ + λ + 4*π
    CE = β + η + ρ + λ
    ET = CE
    EU = 2*ψ
    TU = ψ
    EE = σ + 2*ρ + (β + σ + ρ + λ + π)
    TI = 2*σ
    RV = β + η + σ + ρ + λ + 4*π
    RL = β + η + 2*σ + 5*λ + 2*π
    RS = ρ + π
    CB = β + η + ρ + λ + 4*π
    TF = ω
    CW = α
    BW = α + δ
    BF = 4*ω
    JW = α + μ
    JE = α - 1
    JC = ω
    F = ω + δ + α
    W = μ
    X = 4*EB + 2*EC + 6*SC + 4*S + 2*TI + 2*EU + 2*TU + 2*EE + 2*ET + 4*JE + 8*JC + 4*CW

    print("PC: " + str(PC))
    print("PX: " + str(PX))
    print("BBX: " + str(BBX))
    print("BB11: " + str(BBMAX))
    print("BEX: " + str(BEX))
    print("BE11: " + str(BEMAX))
    print("SC: " + str(SC))
    print("S: " + str(S))
    print("EB: " + str(EB))
    print("EC: " + str(EC))
    print("CE: " + str(CE))
    print("ET: " + str(ET))
    print("EU: " + str(EU))
    print("TU: " + str(TU))
    print("EE: " + str(EE))
    print("TI: " + str(TI))
    print("RV: " + str(RV))
    print("RL: " + str(RL))
    print("RS: " + str(RS))
    print("CB: " + str(CB))
    print("TF: " + str(TF))
    print("CW: " + str(CW))
    print("BW: " + str(BW))
    print("BF: " + str(BF))
    print("JW: " + str(JW))
    print("JE: " + str(JE))
    print("JC: " + str(JC))
    print("F: " + str(F))
    print("W: " + str(W))
    print("X: " + str(X))



convert(5,6,1320,1534,1427,12,97,612,1034,268,268)
