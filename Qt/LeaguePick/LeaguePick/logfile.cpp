#include "logfile.h"
#include <QMessageBox>
#include <QDateTime>
#include <QApplication>

const QString LogFile::_logFileName = "log.txt";
QFile LogFile::_logFile = nullptr;
bool LogFile::_error = false;
bool LogFile::_logInit = false;
QTextStream LogFile::_logTextStream;

LogFile::LogFile()
{

}

void LogFile::write(QString logMsg)
{
    if (_error)
    {
        return;
    }
    if (_logInit == false)
    {
        _logFile.setFileName(_logFileName);
        if (!_logFile.open(QIODevice::WriteOnly | QIODevice::Text | QIODevice::Append))
        {
            QMessageBox::warning(nullptr, QString("Log File"), QString("Log file could not be opened!"));
            _error = true;
            return;
        }
        _logTextStream.setDevice(&_logFile);
        _logInit = true;
    }
    _logTextStream << QDateTime::currentDateTime().toString("yyyy-MM-dd hh:mm:ss.zzz: ") << logMsg << "\n";
}
