// ecosystem.config.js — rss-example
const VENV = "/root/python/rss-example/venv/bin";                 // <— change to your venv bin
const CWD  = "/root/python/rss-example";     // <— change to your repo path

module.exports = {
  apps: [
    {
      name: "redis",
      namespace: "rss",
      script: "/usr/bin/redis-server",
      cwd: CWD,
      autorestart: true,
      log_date_format: "YYYY-MM-DD HH:mm:ss",
      out_file: `${CWD}/logs/redis.out.log`,
      error_file: `${CWD}/logs/redis.err.log`
    },
    {
      name: "celery",
      namespace: "rss",
      script: `${VENV}/celery`,
      interpreter: "none",
      args: "-A tasks.celery_app worker --loglevel=info",
      cwd: CWD,
      env: {
        PYTHONPATH: CWD
      },
      out_file: `${CWD}/logs/celery.out.log`,
      error_file: `${CWD}/logs/celery.err.log`
    },
    {
      name: "uvicorn",
      namespace: "rss",
      script: `${VENV}/uvicorn`,
      interpreter: "none",
      args: "app.main:app --host 0.0.0.0 --port 8000",
      cwd: CWD,
      env: { PYTHONUNBUFFERED: "1" },
      out_file: `${CWD}/logs/uvicorn.out.log`,
      error_file: `${CWD}/logs/uvicorn.err.log`
    }
  ]
};
