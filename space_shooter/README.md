# Space Shooter - Game Restructured

## Cấu trúc thư mục

```
space_shooter/
├── main.py              # Chạy game, vòng lặp chính
├── settings.py          # Hằng số (màu, tốc độ, kích thước)
├── README.md            # File này
│
├── entities/            # Các đối tượng trong game
│   ├── __init__.py
│   ├── player.py        # Lớp Ship (tàu chiến)
│   ├── bullet.py        # Lớp Rocket và Spacemine
│   ├── obstacle.py      # Thiên thạch và hố đen
│   └── effects.py       # Hiệu ứng nổ và powerup
│
├── maps/                # Logic từng màn
│   ├── __init__.py
│   ├── base_map.py      # Lớp cơ sở cho các map
│   ├── deep_space.py    # Map 1: Deep Space Arena
│   ├── gravity_chaos.py # Map 2: Gravity Chaos Zone
│   └── reverse_gravity.py # Map 3: Reverse Gravity Zone
│
├── screens/             # Các màn hình UI
│   ├── __init__.py
│   ├── menu.py          # Menu chính
│   ├── mode_select.py   # Chọn chế độ PvP/PvE
│   ├── map_select.py    # Chọn map
│   └── upgrade_screen.py # Nâng cấp tàu
│
└── resources/           # Dữ liệu game
    ├── asteroids/       # Ảnh thiên thạch
    ├── background*.png  # Background các map
    ├── ship*.png        # Ảnh tàu chiến
    ├── rocket*.png      # Ảnh tên lửa
    ├── *.wav, *.mp3     # Âm thanh
    └── *.ttf            # Font chữ
```

## Cách chạy game

```bash
cd space_shooter
python main.py
```

## Các Map

### Map 1 - Deep Space Arena
- **Tông**: Sạch, cân bằng, học cách chơi
- **Đặc điểm**: 
  - Nền sao cuộn chậm tạo cảm giác đang bay trong không gian
  - Không có gì cản trở — 2 tàu đấu thuần túy kỹ năng
  - Map "tutorial" tự nhiên cho người mới

### Map 2 - Gravity Chaos Zone  
- **Tông**: Hỗn loạn, bất ngờ, đòi hỏi phản xạ
- **Đặc điểm**:
  - Hố đen nằm giữa map liên tục kéo cả 2 tàu vào
  - Thiên thạch trôi lơ lửng xung quanh, vừa là chướng ngại vật vừa có thể dùng làm "lá chắn"
  - Chiến thuật: dụ đối thủ vào vùng hút trong khi mình thoát ra

### Map 3 - Reverse Gravity Zone
- **Tông**: Căng thẳng, nhịp điệu, gây bất ngờ
- **Đặc điểm**:
  - Cứ 15 giây trọng lực lại lật ngược
  - Có cảnh báo trước 2–3 giây để người chơi chuẩn bị
  - Chiến thuật: bắn ngay lúc đối thủ đang mất kiểm soát trong khoảnh khắc đảo chiều

## Chế độ chơi

- **PvP**: 2 người chơi đấu với nhau
  - P1: Mũi tên (di chuyển), Lên (bắn), Xuống (super), Shift (mìn)
  - P2: WASD (di chuyển), W (bắn), S (super), Shift (mìn)

- **PvE**: 1 người chơi vs AI
  - P1: Giống PvP
  - AI: Tự động điều khiển P2, tấn công thông minh

## Yêu cầu

- Python 3.11+
- Pygame

```bash
pip install pygame
```
