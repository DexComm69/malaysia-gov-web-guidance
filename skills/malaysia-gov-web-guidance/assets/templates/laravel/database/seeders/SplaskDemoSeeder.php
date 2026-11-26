<?php

namespace Database\Seeders;

use App\Models\News;
use App\Models\Page;
use Illuminate\Database\Seeder;
use Illuminate\Support\Carbon;

class SplaskDemoSeeder extends Seeder
{
    // Demo content with real dates for trying the template: php artisan db:seed --class=SplaskDemoSeeder
    public function run(): void
    {
        // Times are Malaysia time; Laravel stores them in UTC (config app.timezone).
        $kl = fn ($s) => Carbon::parse($s, 'Asia/Kuala_Lumpur')->utc();
        $pages = [
            ['tentang-kami', 'Tentang Kami', '<p>Latar belakang majlis.</p>', '2026-11-03 09:12:44'],
            ['soalan-lazim', 'Soalan Lazim', '<p>S: Bagaimana membayar cukai taksiran?</p>', '2026-10-01 15:02:10'],
            ['hubungi-kami', 'Hubungi Kami', '<p>Telefon: 03-0000 0000</p>', '2026-11-12 11:30:05'],
            ['dasar-privasi', 'Dasar Privasi', '<p>Kami menghormati privasi anda.</p>', '2026-06-02 10:00:00'],
            ['peta-laman', 'Peta Laman', '<p>Senarai halaman.</p>', '2026-09-14 08:45:00'],
        ];
        foreach ($pages as [$slug, $title, $body, $at]) {
            $p = new Page(['slug' => $slug, 'title' => $title, 'body' => $body]);
            $p->timestamps = false;
            $p->created_at = $p->updated_at = $kl($at);
            $p->save();
        }
        foreach ([['notis-penutupan-jalan', 'Notis penutupan jalan sementara', '2026-11-20 08:05:31'], ['gotong-royong', 'Program gotong-royong perdana', '2026-11-15 09:00:00']] as [$slug, $title, $at]) {
            $n = new News(['slug' => $slug, 'title' => $title, 'body' => '<p>Kandungan berita.</p>']);
            $n->timestamps = false;
            $n->created_at = $n->updated_at = $kl($at);
            $n->save();
        }
    }
}
