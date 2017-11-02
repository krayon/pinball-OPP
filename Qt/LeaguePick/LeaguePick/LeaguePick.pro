#-------------------------------------------------
#
# Project created by QtCreator 2017-10-20T11:30:51
#
#-------------------------------------------------

QT       += core gui

greaterThan(QT_MAJOR_VERSION, 4): QT += widgets

TARGET = LeaguePick
TEMPLATE = app

# The following define makes your compiler emit warnings if you use
# any feature of Qt which has been marked as deprecated (the exact warnings
# depend on your compiler). Please consult the documentation of the
# deprecated API in order to know how to port your code away from it.
DEFINES += QT_DEPRECATED_WARNINGS

# You can also make your code fail to compile if you use deprecated APIs.
# In order to do so, uncomment the following line.
# You can also select to disable deprecated APIs only up to a certain version of Qt.
#DEFINES += QT_DISABLE_DEPRECATED_BEFORE=0x060000    # disables all the APIs deprecated before Qt 6.0.0

# win32:CONFIG(release, debug|release): LIBS += -L$$quote(C:/Program Files/Microsoft SDKs/Windows/v7.0/Lib/)
# else:win64:CONFIG(release, debug|release): LIBS += -L$$quote(C:/Program Files/Microsoft SDKs/Windows/v7.0/Lib/x64/)
LIBS += -L$$quote(C:/Program Files/Microsoft SDKs/Windows/v7.0/Lib/)

SOURCES += \
        main.cpp \
        mainwindow.cpp \
    logfile.cpp \
    player.cpp \
    season.cpp \
    playervm.cpp \
    seasonplayersvm.cpp \
    meet.cpp \
    crtmeetvm.cpp \
    last.cpp

HEADERS += \
        mainwindow.h \
    logfile.h \
    player.h \
    season.h \
    playervm.h \
    seasonplayersvm.h \
    meet.h \
    crtmeetvm.h \
    last.h

FORMS += \
        mainwindow.ui

CONFIG += mobility
CONFIG += c++11

MOBILITY = 

