export LC_ALL=C.UTF-8
export LANG=C.UTF-8

# export FN_AUTH_REDIRECT_URI=http://ec2-13-125-217-77.ap-northeast-2.compute.amazonaws.com:7070/google/auth
# export FN_BASE_URI=http://ec2-13-125-217-77.ap-northeast-2.compute.amazonaws.com:7070

export FN_AUTH_REDIRECT_URI=http://10.30.7.19.nip.io:7070/google/auth
export FN_BASE_URI=http://10.30.7.19.nip.io:7070

export FN_CLIENT_ID=your_OAuth2.0_FN_CLIENT_ID
export FN_CLIENT_SECRET=your_OAuth2.0_CLIENT_SECRET

export FLASK_APP=app.py

export FLASK_DEBUG=0
export FN_FLASK_SECRET_KEY=SOMETHING RANDOM AND SECRET

export TMPDIR=$HOME/tmp

python3 -m flask run -h 0.0.0.0 -p 7070
