# iBlueTeam: Detection Coverage Matrix

MITRE ATT&CK matrisi üzərində detection əhatəsini göstərən komanda platforması. Əhatə statusu əl ilə seçilmir, qaydalardan, test nəticələrindən və log mənbələrinin vəziyyətindən hesablanır.

- **Backend:** Python, FastAPI, SQLAlchemy, SQLite (`data/ibluteam.db`)
- **Frontend:** HTML, CSS, vanilla JS (build addımı yoxdur)
- **Verilənlər:** ATT&CK Enterprise (MITRE-in rəsmi STIX faylı), sintetik nümunə qaydalar və test qeydləri

## İşə salmaq (təmiz mühit)

```bash
python -m venv .venv && source .venv/bin/activate     # Windows: .venv\Scripts\activate
pip install -r requirements.txt
IBT_ADMIN_PASSWORD='sizin-parolunuz' python run.py     # Windows PowerShell: $env:IBT_ADMIN_PASSWORD='...'; python run.py
```

Brauzerdə açın: http://127.0.0.1:8000 (giriş: `admin` və verdiyiniz parol).

- `IBT_ADMIN_PASSWORD` verilməsə, ilk işə salmada təsadüfi parol yaradılıb konsola bir dəfə çap olunur.
- **MITRE ATT&CK dataset:** `data/enterprise-attack.json` is intentionally excluded from this GitHub repository because it exceeds GitHub’s 25 MB browser-upload limit. On the first launch, iBlueTeam automatically attempts to download the official MITRE ATT&CK Enterprise STIX dataset and import it into the local SQLite database. An internet connection is required for this automatic download. If the download fails, the application uses a limited built-in fallback dataset instead of the complete ATT&CK matrix.
- **Manual setup (offline or failed download):** Download [`enterprise-attack.json`](https://raw.githubusercontent.com/mitre/cti/master/enterprise-attack/enterprise-attack.json) from the official [MITRE CTI repository](https://github.com/mitre/cti), save it as `data/enterprise-attack.json`, then run `python run.py --reimport-attack` from the project root. This imports the full dataset into the local database. The dataset is excluded by `.gitignore` and should not be committed to GitHub.
- **Note:** `--reimport-attack` forces a fresh import. If the local JSON file is absent, the application attempts to download it first; without internet access, it falls back to the limited built-in dataset.
- Köhnə `data/ibluteam.db` faylınız varsa saxlayın: açılışda avtomatik yenilənir, məlumat itmir.
- Eyni şəbəkədəki cihazlar (telefon, honeypot VM) üçün: `python run.py --lan` (cmd-də qoşulma ünvanları yazılır). Şəbəkədəki hər kəs baxa bilər, dəyişiklik üçün giriş lazımdır.
- Seçimlər: `--port 9000`, `--no-sample` (nümunə qaydalar olmadan), `--reimport-attack`, `--reload`.
- Mühit dəyişənləri: `IBT_ADMIN_PASSWORD`, `IBT_SECRET` (token açarı), `IBT_TARGET_NAME`, `IBT_TARGET_LAT`, `IBT_TARGET_LON` (monitor xəritəsində qorunan şəbəkənin yeri).
- İnteraktiv API sənədi: http://127.0.0.1:8000/docs

## Səhifələr

| Səhifə | Məzmun |
|---|---|
| **Matris** | Taktikalar üzrə sütunlar, status rəngləri, **heatmap rejimi**, taktika və ümumi əhatə faizi, risk-çəkili əhatə, kor texnikalar, axtarış və filtr (taktika adı, status, platforma), alt-texnikalar |
| **Monitor** | **Live Detection Monitor**: dünya xəritəsində sintetik hadisə axını (aşkarlandı, qismən, qaçırıldı), canlı axın siyahısı, ən təhlükəli boşluqlar |
| **Honeypot** | Açıq portlara gələn real skan və hücumlar: statistika, sensor açarı, simulyasiya, quraşdırma əmri, hadisə cədvəli. Hadisələr ATT&CK texnikalarına uyğunlaşdırılır, Monitor-da «Honeypot» rejimində, matrisdə və boşluq balında görünür. Ətraflı: [docs/honeypot.md](docs/honeypot.md) |
| **Qaydalar** | Qayda siyahısı, əlavə, redaktə, silmə, log mənbəyi bağlama, **test qeydləri**, Sigma YAML və CSV idxalı |
| **Mənbələr** | Log mənbəyi kataloqu: hansı mənbə toplanır. Toplanmayan mənbə qaydanı «kor» edir |
| **Boşluqlar** | Prioritet balına görə sıralanmış boşluqlar, səbəb, filtrlər, CSV ixracı |
| **İcmal** | Ümumi faiz, taktika üzrə əhatə, qayda, test və log mənbəyi statistikası |

Texnikaya klik edəndə yan panel açılır: təsvir, lazım olan log mənbələri, bağlı qaydalar, test qeydləri, alt-texnikalar, qeydlər.

**Giriş:** oxumaq üçün giriş lazım deyil. Qayda, test, qeyd, log mənbəyi və idxal dəyişiklikləri yalnız daxil olmuş istifadəçi üçündür. Admin istifadəçi əlavə edə bilər (topbar → istifadəçi menyusu).

**İxrac:** topbar-da «İxrac» menyusu: Matris JSON, Matris CSV, Boşluqlar CSV, ATT&CK Navigator layer.

## Əhatə necə hesablanır

Qısa xülasə (tam sənəd: [docs/coverage.md](docs/coverage.md)):

| Vəziyyət | Şərt |
|---|---|
| Tam | ən azı bir qayda **aktivdir, son testi uğurludur və bütün log mənbələri toplanır** |
| Qismən | qayda var, amma draft, test olunmamış, son test uğursuz və ya log mənbəyi göstərilməyib |
| Boşluq | qayda yoxdur, söndürülüb və ya log mənbəyi toplanmır |
| Kor | boşluq və səbəb telemetriyadır (qayda var, amma mənbə toplanmır, ya da ATT&CK-ın tələb etdiyi mənbələrin heç biri toplanmır) |

## Sənədlər

- [docs/architecture.md](docs/architecture.md): arxitektur sxemi, məlumat axını, təhlükəsizlik
- [docs/data-model.md](docs/data-model.md): data modeli və API xülasəsi
- [docs/coverage.md](docs/coverage.md): coverage hesablama qaydası, heatmap balı, boşluq balı
- [docs/honeypot.md](docs/honeypot.md): honeypot quraşdırması, təsnifat, təhlükəsizlik
- [docs/demo.md](docs/demo.md): demo ssenarisi

## Qovluq quruluşu

```
honeypot/  honeypot.py (sensor agenti), sim_client.py (sınaq trafiki)
backend/   main.py (API), honeypot.py, geo.py, models.py, coverage.py, auth.py, monitor.py, attack_import.py, sigma.py, seed*.py
frontend/  index.html, css/style.css, js/ (matrix, monitor, honeypot, rules, sources, gaps, overview, panel, auth)
data/      ATT&CK JSON, nümunə qaydalar. SQLite faylı və gizli açar işə salınanda yaranır (repoya düşmür)
docs/      arxitektur, data modeli, coverage qaydası, demo
```

## Məhdudiyyətlər

- SIEM inteqrasiyası yoxdur. Honeypot real trafik üçün açıq IP-li ayrıca VM tələb edir (platformadan kənarda qurulur). Qaydalar və log mənbəyi vəziyyəti əl ilə və ya fayl ilə daxil edilir. Monitor sintetik hadisələrlə işləyir.
- Qaydalar platformaya bağlı deyil: qayda texnikaya bağlanır, texnika bir neçə platformada varsa, əhatə bu platformaların hamısında sayılır.
- SQLite az sayda eyni vaxtlı istifadəçi üçün kifayətdir. PostgreSQL-ə keçid `backend/database.py`-dakı bağlantı sətrini dəyişməklə olur.
- Şriftlər Google Fonts-dan yüklənir. İnternet yoxdursa, sistem şrifti istifadə olunur.
