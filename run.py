import uvicorn


if __name__ == '__main__':
    uvicorn.run('main:app',
                host='0.0.0.0',
                port=8001,
                reload=True,
                access_log=False,
                timeout_keep_alive=0,
                debug=True)
