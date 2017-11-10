#include "meet.h"
#include "season.h"

#include "logfile.h"

#include <QFile>
#include <QTextStream>
#include <QMessageBox>

#include <string>
#include <sstream>
#include <iomanip>

QString Meet::_meetFileName;
std::vector<Meet::MeetInfo> Meet::_meetVect;
int Meet::_numMeets = 0;
bool Meet::_changesMade = false;
int Meet::currMeet = 0;
int Meet::newMeet = 0;

Meet::Meet()
{

}

std::vector<Meet::MeetInfo> Meet::read()
{
    write();
    _numMeets = 0;
    _meetFileName = QString("meet.%1.txt").arg(Season::currSeason, 3, 10, QChar('0'));
    _meetVect.clear();

    QFile file(_meetFileName);

    if (!file.open(QIODevice::ReadOnly | QIODevice::Text))
    {
        // No warning message since this is normal if no meets in season
        return (_meetVect);
    }

    QTextStream in(&file);
    while (!in.atEnd())
    {
        QString line(in.readLine());
        std::stringstream lineStrStream(line.toStdString());
        std::string field;
        std::vector<std::string> fieldVect;
        MeetInfo tmpMeet;

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
            QString errorStr("Meet file line does not contain enough fields!  " + line);

            LogFile::write(errorStr);
            QMessageBox::critical(nullptr, "Meet File Field error", errorStr);
            exit(-1);
        }

        int retCode;

        retCode = sscanf(fieldVect[_UID_IDX].c_str(), "%d", &tmpMeet.uid);
        if (retCode != 1)
        {
            QString errorStr("Could not convert unique ID!  " + line);

            LogFile::write(errorStr);
            QMessageBox::critical(nullptr, "Meet File UID convert error", errorStr);
            exit(-1);
        }
        if (tmpMeet.uid != _numMeets)
        {
            QString errorStr("Meet file UIDs should be contiguous starting at 0!  " + line);

            LogFile::write(errorStr);
            QMessageBox::critical(nullptr, "Meet File UID error", errorStr);
            exit(-1);
        }
        _numMeets++;

        tmpMeet.meetName = QString::fromStdString(fieldVect[_MEET_NAME_IDX]);
        _meetVect.push_back(tmpMeet);

    }
    file.close();
    return (_meetVect);
}

void Meet::write()
{
    if (_changesMade)
    {
        QFile file(_meetFileName);

        if (!file.open(QIODevice::WriteOnly | QIODevice::Text))
        {
            QString errorStr("Meet file could not be opened for writing.");

            LogFile::write(errorStr);
            QMessageBox::critical(nullptr, "Meet File", errorStr);
            return;
        }

        QTextStream outTxtStream(&file);
        for (auto &iter : _meetVect)
        {
            outTxtStream << iter.uid << "$" << iter.meetName << "$" << endl;
        }
        file.close();
        _changesMade = false;
    }
}

bool Meet::addMeet(QString meetName)
{
    MeetInfo tmpMeet;

    if (meetName == "")
    {
        QMessageBox::warning(nullptr, "Meet Name", "Meet name must be filled out.");
        return false;
    }

    // Check if this is the meet to be added
    tmpMeet.uid = _numMeets++;
    tmpMeet.meetName = meetName;

    _meetVect.push_back(tmpMeet);

    _changesMade = true;
    return true;
}

int Meet::getUID(QString meetName)
{
    for (auto &iter : _meetVect)
    {
        if (meetName == iter.meetName)
        {
            return iter.uid;
        }
    }

    QString errorStr("Meet name UID not found.  Software failure.");

    LogFile::write(errorStr);
    QMessageBox::critical(nullptr, "Software fail", errorStr);
    exit(-1);
}

void Meet::removeLastMeet()
{
    _numMeets--;
    _meetVect.erase(_meetVect.begin() + _numMeets);
    if (Meet::currMeet == Meet::newMeet)
    {
        Meet::currMeet--;
    }
}
