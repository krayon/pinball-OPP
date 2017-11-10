#include "logfile.h"

#include "season.h"
#include "player.h"

#include <QFile>
#include <QTextStream>
#include <QMessageBox>

#include <string>
#include <sstream>
#include <iomanip>

const QString Season::_seasonFileName = "season.txt";
std::vector<Season::SeasonInfo> Season::_seasonVect;
bool Season::_changesMade = false;
int Season::_maxUid = 0;
int Season::currSeason = 0;

Season::Season()
{

}

std::vector<Season::SeasonInfo> Season::read()
{
    QFile file(_seasonFileName);

    if (!file.open(QIODevice::ReadOnly | QIODevice::Text))
    {
        QString errorStr("Season file could not be opened for reading.");

        LogFile::write(errorStr);
        QMessageBox::warning(nullptr, "Season File", errorStr);
        return (_seasonVect);
    }

    QTextStream in(&file);
    while (!in.atEnd())
    {
        QString line(in.readLine());
        std::stringstream lineStrStream(line.toStdString());
        std::string field;
        std::vector<std::string> fieldVect;
        std::vector<std::string> bfVect;
        SeasonInfo tmpSeason;
        std::stringstream bfStrStream;

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
            QString errorStr("Season file line does not contain enough fields!  " + line);

            LogFile::write(errorStr);
            QMessageBox::critical(nullptr, "Season File Field error", errorStr);
            exit(-1);
        }

        int retCode;
        int tmpVal;

        retCode = sscanf(fieldVect[_UID_IDX].c_str(), "%d", &tmpSeason.uid);
        if (retCode != 1)
        {
            QString errorStr("Could not convert unique ID!  " + line);

            LogFile::write(errorStr);
            QMessageBox::critical(nullptr, "Season File UID convert error", errorStr);
            exit(-1);
        }

        if (tmpSeason.uid > _maxUid)
        {
            _maxUid = tmpSeason.uid;
        }

        tmpSeason.seasonName = QString::fromStdString(fieldVect[_SEASON_NAME_IDX]);

        bfStrStream.str(fieldVect[_PLAYER_BF_IDX]);
        while (std::getline(bfStrStream, field, ','))
        {
           bfVect.push_back(field);
        }
        for(auto const& value: bfVect)
        {
            retCode = sscanf(value.c_str(), "0x%x", &tmpVal);
            if (retCode != 1)
            {
                QString errorStr("Could not convert player bitfield!  " + line);

                LogFile::write(errorStr);
                QMessageBox::warning(nullptr, "Season File player bitfield convert error", errorStr);
            }
            tmpSeason.playerBF.push_back(tmpVal);
        }

        bfVect.clear();
        bfStrStream.clear();
        bfStrStream.str(fieldVect[_PAID_BF_IDX]);
        while (std::getline(bfStrStream, field, ','))
        {
           bfVect.push_back(field);
        }
        for(auto const& value: bfVect)
        {
            retCode = sscanf(value.c_str(), "0x%x", &tmpVal);
            if (retCode != 1)
            {
                QString errorStr("Could not convert paid bitfield!  " + line);

                LogFile::write(errorStr);
                QMessageBox::warning(nullptr, "Season File paid bitfield convert error", errorStr);
            }
            tmpSeason.paidBF.push_back(tmpVal);
        }

        _seasonVect.push_back(tmpSeason);

    }
    file.close();
    return (_seasonVect);
}

void Season::write()
{
    if (_changesMade)
    {
        QFile file(_seasonFileName);

        if (!file.open(QIODevice::WriteOnly | QIODevice::Text))
        {
            QString errorStr("Season file could not be opened for writing.");

            LogFile::write(errorStr);
            QMessageBox::critical(nullptr, "Season File", errorStr);
            return;
        }

        QTextStream outTxtStream(&file);
        for (auto &iter : _seasonVect)
        {
            outTxtStream << iter.uid << "$" << iter.seasonName << "$";
            for (int index = 0; index < (Player::getNumPlyrs())/32 + 1; index++)
            {
                if (index != 0)
                {
                    outTxtStream << ",";
                }
                outTxtStream << QString("0x%1").arg(iter.playerBF[index], 8, 16, QChar('0'));
            }
            outTxtStream << "$";
            for (int index = 0; index < (Player::getNumPlyrs())/32 + 1; index++)
            {
                if (index != 0)
                {
                    outTxtStream << ",";
                }
                outTxtStream << QString("0x%1").arg(iter.paidBF[index], 8, 16, QChar('0'));
            }
            outTxtStream << "$" << endl;
        }
        file.close();
    }
}

bool Season::addSeason(QString seasonName)
{
    SeasonInfo tmpSeason;

    if (seasonName == "")
    {
        QMessageBox::warning(nullptr, "Season Name", "Season name must be filled out.");
        return false;
    }

    tmpSeason.uid = ++_maxUid;
    tmpSeason.seasonName = seasonName;
    for (int index = 0; index < (Player::getNumPlyrs())/32 + 1; index++)
    {
        tmpSeason.paidBF.push_back(0);
        tmpSeason.playerBF.push_back(0);
    }

    _seasonVect.push_back(tmpSeason);

    _changesMade = true;
    return true;
}

int Season::getUID(QString seasonName)
{
    for (auto &iter : _seasonVect)
    {
        if (seasonName == iter.seasonName)
        {
            return iter.uid;
        }
    }

    QString errorStr("Season name UID not found.  Software failure.");

    LogFile::write(errorStr);
    QMessageBox::critical(nullptr, "Software fail", errorStr);
    exit(-1);
}

void Season::updateName(int seasonUid, QString seasonName)
{
    for (auto &iter : _seasonVect)
    {
        if (seasonUid == iter.uid)
        {
            iter.seasonName = seasonName;
            _changesMade = true;
            return;
        }
    }
}

bool Season::isActPlyr(int seasonUid, int plyrUid)
{
    if (_seasonVect.size() != 0)
    {
        int bit = plyrUid & 0x1f;
        int index = plyrUid >> 5;

        return ((_seasonVect[seasonUid].playerBF[index] & (1 << bit)) ? true: false);
    }
    return (false);
}

bool Season::isPaid(int seasonUid, int plyrUid)
{
    if (_seasonVect.size() != 0)
    {
        int bit = plyrUid & 0x1f;
        int index = plyrUid >> 5;

        return ((_seasonVect[seasonUid].paidBF[index] & (1 << bit)) ? true: false);
    }
    return (false);
}

void Season::setActPlyr(int seasonUid, int plyrUid, bool flag)
{
    int bit = plyrUid & 0x1f;
    int index = plyrUid >> 5;

    if (flag)
    {
        _seasonVect[seasonUid].playerBF[index] |= (1 << bit);
    }
    else
    {
        _seasonVect[seasonUid].playerBF[index] &= ~(1 << bit);
    }
    _changesMade = true;
}

void Season::setPaid(int seasonUid, int plyrUid, bool flag)
{
    int bit = plyrUid & 0x1f;
    int index = plyrUid >> 5;

    if (flag)
    {
        _seasonVect[seasonUid].paidBF[index] |= (1 << bit);
    }
    else
    {
        _seasonVect[seasonUid].paidBF[index] &= ~(1 << bit);
    }
    _changesMade = true;
}

void Season::addPlyr()
{
    // If just starting, no season will be configured
    if (_seasonVect.size() != 0)
    {
        if ((unsigned)(Player::getNumPlyrs()/32 + 1) > _seasonVect[0].playerBF.size())
        {
            for (auto &iter : _seasonVect)
            {
                iter.playerBF.push_back(0);
                iter.paidBF.push_back(0);
            }
        }
    }
}

std::vector<int> Season::getActPlyrLst()
{
    std::vector<int> actPlyrLst;

    for (auto &iter : _seasonVect[currSeason].playerBF)
    {
        for (int index = 0; index < 32; index++)
        {
            if ((iter & (1 << index)) != 0)
            {
                actPlyrLst.push_back(index);
            }
        }
    }
    return (actPlyrLst);
}
