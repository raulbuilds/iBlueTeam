import argparse
import socket
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from backend import models                                                  
from backend.attack_import import ensure_attack              
from backend.auth import ensure_admin              
from backend.database import SessionLocal              
from backend.migrate import ensure_schema              
from backend.seed import seed_sample_rules              


def lan_ips():
    ips = []
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("10.255.255.255", 1))                                                                       
        ips.append(s.getsockname()[0])
        s.close()
    except OSError:
        pass
    try:
        for info in socket.getaddrinfo(socket.gethostname(), None, socket.AF_INET):
            if info[4][0] not in ips:
                ips.append(info[4][0])
    except OSError:
        pass
    return [ip for ip in ips if not ip.startswith("127.")]


def main():
    ap = argparse.ArgumentParser(description="iBlueTeam: Detection Coverage Matrix")
    ap.add_argument("--host", default="127.0.0.1")
    ap.add_argument("--port", type=int, default=8000)
    ap.add_argument("--lan", action="store_true", help="eyni şəbəkədəki cihazlar (telefon, honeypot VM) üçün aç və IP ünvanlarını göstər")
    ap.add_argument("--no-sample", action="store_true", help="nümunə qaydaları yükləmə")
    ap.add_argument("--reimport-attack", action="store_true", help="ATT&CK məlumatını yenidən yüklə")
    ap.add_argument("--reload", action="store_true", help="kod dəyişəndə serveri yenidən başlat")
    args = ap.parse_args()
    if args.lan:
        args.host = "0.0.0.0"

    ensure_schema()
    with SessionLocal() as db:
        pw = ensure_admin(db)
        if pw:
            print(f"\n  Admin hesabı yaradıldı: admin / {pw}\n  (parolu dəyişmək üçün IBT_ADMIN_PASSWORD mühit dəyişəni ilə yeni bazadan başlayın)\n")
        print("ATT&CK:", ensure_attack(db, force=args.reimport_attack))
        if not args.no_sample:
            n = seed_sample_rules(db)
            if n:
                print(f"Nümunə: {n} qayda yükləndi")

    import uvicorn

    if args.host == "0.0.0.0":
        print("\n  iBlueTeam hazırdır. Eyni şəbəkədəki cihazlardan bu ünvanla açın:")
        for ip in lan_ips():
            print(f"    http://{ip}:{args.port}")
        print(f"  Bu kompüterdə: http://127.0.0.1:{args.port}\n")
    else:
        print(f"\n  iBlueTeam hazırdır: http://{args.host}:{args.port}\n")
    uvicorn.run("backend.main:app", host=args.host, port=args.port, reload=args.reload)


if __name__ == "__main__":
    main()
