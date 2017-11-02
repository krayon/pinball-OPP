#include "last.h"
#include "season.h"
#include "meet.h"
#include "logfile.h"

#include <QFile>
#include <QTextStream>
#include <QMessageBox>

#include <string>
#include <sstream>
#include <iomanip>

const QString Last::_lastFileName = "last.txt";

Last::Last()
{

}

void Last::read(int& season, int& meet)
{
    QFile file(_lastFileName);

    if (!file.open(QIODevice::ReadOnly | QIODevice::Text))
    {
        QString errorStr("Last file could not be opened for reading.");

        LogFile::write(errorStr);
        QMessageBox::warning(nullptr, "Last File", errorStr);
        season = 0;
        meet = 0;
        return;
    }

    QTextStream in(&file);
    while (!in.atEnd())
    {
        QString line(in.readLine());
        std::stringstream lineStrStream(line.toStdString());
        std::string field;
        std::vector<std::string> fieldVect;

        while(std::getline(lineStrStream, field, '$'))
        {
           fieldVect.push_back(field);
        }

        // If no fields, just ignore this line
        if (fieldVect.size() == 0)
        {
            break;
        }

        // Check if there are enough fields
        if (fieldVect.size() != _NUM_COLUMNS)
        {
            QString errorStr("Last file does not contain enough fields!  " + line);

            LogFile::write(errorStr);
            QMessageBox::critical(nullptr, "Last File Field error", errorStr);
            exit(-1);
        }

        try
        {
            season = stoi(fieldVect[_SEASON_IDX], nullptr);
        }
        catch (...)
        {
            QString errorStr("Could not convert season ID!  " + line);

            LogFile::write(errorStr);
            QMessageBox::critical(nullptr, "Last File season ID convert error", errorStr);
            exit(-1);
        }

        try
        {
            meet = stoi(fieldVect[_MEET_IDX], nullptr);
        }
        catch (...)
        {
            QString errorStr("Could not convert meet ID!  " + line);

            LogFile::write(errorStr);
            QMessageBox::critical(nullptr, "Last File meet ID convert error", errorStr);
            exit(-1);
        }
    }
    file.close();
}

void Last::write()
{
    QFile file(_lastFileName);

    if (!file.open(QIODevice::WriteOnly | QIODevice::Text))
    {
        QString errorStr("Last file could not be opened for writing.");

        LogFile::write(errorStr);
        QMessageBox::critical(nullptr, "Last File", errorStr);
        return;
    }

    QTextStream outTxtStream(&file);
    outTxtStream << Season::currSeason << "$" << Meet::currMeet << "$";
    file.close();
}
