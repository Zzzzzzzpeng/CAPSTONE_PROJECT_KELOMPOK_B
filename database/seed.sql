INSERT INTO ikan (
    id,
    nama,
    foto,
    kategori,
    jumlah,
    harga
)
VALUES
    (1,  'Arwana',          '/assets/images/Arwana.jpg',         'Predator',    5,   5000000),
    (2,  'Guppy',           '/assets/images/Guppy.jpg',          'Hias Kecil',  150, 50000),
    (3,  'Cupang Avatar',   '/assets/images/Cupang avatar.jpg', 'Cupang',      200, 10000),
    (4,  'Gibicep',         '/assets/images/Gibicep.jpg',        'Pembersih',   200, 50000),
    (5,  'Molly Platinum',  '/assets/images/Molly platinum.jpg', 'Molly',       300, 5000),
    (6,  'Glowfish',        '/assets/images/Glowfish.jpg',       'Hias Kecil',  500, 50000),
    (7,  'Koki Jumbo',      '/assets/images/Koki jumbo.jpg',     'Koki',        80,  200000),
    (8,  'Oscar Red',       '/assets/images/Oscar red.jpg',      'Predator',    12,  800000),
    (9,  'Oscar Tiger',     '/assets/images/Oscar Tiger.jpg',    'Predator',    12,  600000),
    (10, 'Molly Gold',      '/assets/images/Molly gold.jpg',     'Molly',       35,  10000),
    (11, 'Koi Kabuto',      '/assets/images/Koi Kabuto.jpg',     'Koi',         150, 15000),
    (12, 'Ninetine',        '/assets/images/Ninetine.jpg',       'Hias Kecil',  25,  15000),
    (13, 'Koki Panda',      '/assets/images/Koki panda.jpg',     'Koki',        99,  50000),
    (14, 'Sapu Sapu',       '/assets/images/Sapu sapu.jpg',     'Pembersih',   30,  20000),
    (15, 'Louhan',          '/assets/images/Louhan.jpg',         'Predator',    8,   350000),
    (16, 'Cupang Halfmon',  '/assets/images/Cupang halfmon.jpg','Cupang',      100, 10000),
    (17, 'Molly Multi',     '/assets/images/Molly multi.jpg',    'Molly',       40,  6000),
    (18, 'Molly Oren',      '/assets/images/Molly Oren.jpg',     'Molly',       40,  6000),
    (19, 'Golden Black',    '/assets/images/Golden black.jpg',   'Molly',       390, 5000),
    (20, 'Sumatra',         '/assets/images/Sumatra.jpg',        'Hias Kecil',  300, 5000),
    (21, 'Chana Asiatika',  '/assets/images/Chana asiatika.jpg', 'Channa',      50,  50000),
    (22, 'Chana Albino',    '/assets/images/Chana albino.jpg',   'Channa',      50,  60000),
    (23, 'Lobster Warna',   '/assets/images/Lobster warna.jpg',  'Crustacea',   370, 16000),
    (24, 'Sinodentis',      '/assets/images/Sinodentis.jpg',    'Pembersih',   150, 10000),
    (25, 'Koi Kohaku',      '/assets/images/Koi kohaku.jpg',    'Koi',         200, 16000),
    (26, 'Koki Oranda',     '/assets/images/Koki Oranda.jpg',   'Koki',        25,  50000),
    (27, 'Molly Marbel',    '/assets/images/Molly marbel.jpg',  'Molly',       350, 5000),
    (28, 'Pbas',            '/assets/images/Pbas.jpg',          'Predator',    50,  100000),
    (29, 'Koi Shushui',     '/assets/images/Koi shushui.jpg',   'Koi',         120, 95000),
    (30, 'Manfish',         '/assets/images/Manfish.jpg',        'Hias',        99,  15000),
    (31, 'Gurame Padang',   '/assets/images/Gurame Padang.jpg',  'Hias Besar',  140, 40000)
ON CONFLICT (id)
DO UPDATE SET
    nama = EXCLUDED.nama,
    foto = EXCLUDED.foto,
    kategori = EXCLUDED.kategori,
    jumlah = EXCLUDED.jumlah,
    harga = EXCLUDED.harga,
    updated_at = NOW();

-- Penting:
-- INSERT dengan ID eksplisit tidak otomatis menaikkan identity sequence.
SELECT setval(
    pg_get_serial_sequence('ikan', 'id'),
    GREATEST(
        COALESCE((SELECT MAX(id) FROM ikan), 1),
        1
    ),
    true
);
