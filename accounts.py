import urllib.request
import pandas as pd
import re
from bs4 import BeautifulSoup


def hasSocialService(displayName, socialService):
    return len(displayName.find_all("img", attrs={"alt": socialService})) > 0


cybozuConnpassUrl = 'https://cybozu.connpass.com/participation/'
userData = pd.DataFrame(
    {}, columns=['userId', 'hasTwitter', 'hasFacebook', 'hasGitHub'])

pageNumber = 1

while True:
    params = {
        'page': pageNumber,
    }
    req = urllib.request.Request('{}?{}'.format(
        cybozuConnpassUrl, urllib.parse.urlencode(params)))
    with urllib.request.urlopen(req) as req:
        responseBody = req.read()
        soup = BeautifulSoup(responseBody, 'lxml')

    displayNames = soup.find_all(
        "p", attrs={"class": "GroupMemberDisplayName"})
    for displayName in displayNames:
        href = displayName.a.get("href")
        m = re.match("https://connpass.com/user/(.*)/", href)
        if m is None:
            continue
        userId = m.groups()[0]
        hasTwitter = hasSocialService(displayName, "Twitter")
        hasFacebook = hasSocialService(displayName, "Facebook")
        hasGitHub = hasSocialService(displayName, "GitHub")
        userData.loc[userId] = [userId, hasTwitter, hasFacebook, hasGitHub]
    if len(soup.find_all("a", text=re.compile(">>"))) == 0:
        break
    pageNumber += 1
userData.to_csv('accounts.csv')
