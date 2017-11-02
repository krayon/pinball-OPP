#include "logfile.h"

#include "player.h"

#include <QFile>
#include <QTextStream>
#include <QMessageBox>

#include <string>
#include <sstream>

const QString Player::_plyrFileName = "player.txt";
std::vector<Player::PlayerInfo> Player::_plyrVect;
bool Player::_changesMade = false;
int Player::_numPlyrs = 0;

Player::Player()
{

}

void Player::read()
{
    QFile file(_plyrFileName);

    if (!file.open(QIODevice::ReadOnly | QIODevice::Text))
    {
        QString errorStr("Player file could not be opened for reading.");

        LogFile::write(errorStr);
        QMessageBox::warning(nullptr, "Player File", errorStr);
        return;
    }

    QTextStream in(&file);
    while (!in.atEnd())
    {
        QString line(in.readLine());
        std::stringstream lineStrStream(line.toStdString());
        std::string field;
        std::vector<std::string> fieldVect;
        PlayerInfo currPlyr;

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
            QString errorStr("Player file line does not contain enough fields!  " + line);

            LogFile::write(errorStr);
            QMessageBox::critical(nullptr, "Player File Field error", errorStr);
            exit(-1);
        }

        try
        {
            currPlyr.uid = stoi(fieldVect[_UID_IDX], nullptr);
            if (currPlyr.uid != _numPlyrs)
            {
                QString errorStr("Player file UIDs should be contiguous starting at 0!  " + line);

                LogFile::write(errorStr);
                QMessageBox::critical(nullptr, "Player File UID error", errorStr);
                exit(-1);
            }
            _numPlyrs++;
        }
        catch (...)
        {
            QString errorStr("Could not convert unique ID!  " + line);

            LogFile::write(errorStr);
            QMessageBox::critical(nullptr, "Player File UID convert error", errorStr);
            exit(-1);
        }

        currPlyr.lastName = QString::fromStdString(fieldVect[_LAST_NAME_IDX]);
        currPlyr.firstName = QString::fromStdString(fieldVect[_FIRST_NAME_IDX]);
        currPlyr.email = QString::fromStdString(fieldVect[_EMAIL_IDX]);
        currPlyr.phoneNum = QString::fromStdString(fieldVect[_PHONE_NUM_IDX]);

        _plyrVect.push_back(currPlyr);

    }
    file.close();
}

void Player::write()
{
    QFile file(_plyrFileName);

    if (!file.open(QIODevice::WriteOnly | QIODevice::Text))
    {
        QString errorStr("Player file could not be opened for writing.");

        LogFile::write(errorStr);
        QMessageBox::critical(nullptr, "Player File", errorStr);
        return;
    }

    QTextStream outTxtStream(&file);
    for (auto &iter : _plyrVect)
    {
        outTxtStream << iter.uid << "$" << iter.lastName << "$" << iter.firstName << \
                     "$" << iter.email << "$" << iter.phoneNum << "$" << endl;
    }
    file.close();
}

int Player::getNumPlyrs()
{
    return _numPlyrs;
}

QString Player::getLastName(int plyrUid)
{
    return (_plyrVect[plyrUid].lastName);
}
QString Player::getFirstName(int plyrUid)
{
    return (_plyrVect[plyrUid].firstName);
}
QString Player::getEmail(int plyrUid)
{
    return (_plyrVect[plyrUid].email);
}
QString Player::getPhone(int plyrUid)
{
    return (_plyrVect[plyrUid].phoneNum);
}

void Player::setLastName(int plyrUid, QString data)
{
    if (_plyrVect[plyrUid].lastName != data)
    {
        _plyrVect[plyrUid].lastName = data;
        _changesMade = true;
    }
}
void Player::setFirstName(int plyrUid, QString data)
{
    if (_plyrVect[plyrUid].firstName != data)
    {
        _plyrVect[plyrUid].firstName = data;
        _changesMade = true;
    }
}
void Player::setEmail(int plyrUid, QString data)
{
    if (_plyrVect[plyrUid].email != data)
    {
        _plyrVect[plyrUid].email = data;
        _changesMade = true;
    }
}
void Player::setPhone(int plyrUid, QString data)
{
    if (_plyrVect[plyrUid].phoneNum != data)
    {
        _plyrVect[plyrUid].phoneNum = data;
        _changesMade = true;
    }
}

bool Player::addPlayer(QString lastName, QString firstName, QString phoneNum,
    QString email)
{
    PlayerInfo currPlyr;

    if ((firstName == "") || (lastName == ""))
    {
        QMessageBox::warning(nullptr, "Player First/Last Name", "Player first and last name must be filled out.");
        return false;
    }

    currPlyr.uid = _numPlyrs++;
    currPlyr.lastName = lastName;
    currPlyr.firstName = firstName;
    currPlyr.email = email;
    currPlyr.phoneNum = phoneNum;

    _plyrVect.push_back(currPlyr);

    _changesMade = true;
    return true;
}
