#ifndef LOGFILE_H
#define LOGFILE_H

#include <QString>
#include <QFile>
#include <QTextStream>

class LogFile
{
    public:
        LogFile();
        static void write(QString logMsg);

    private:
        static const QString _logFileName;
        static QFile _logFile;
        static QTextStream _logTextStream;
        static bool _error;
        static bool _logInit;
};

#endif // LOGFILE_H
