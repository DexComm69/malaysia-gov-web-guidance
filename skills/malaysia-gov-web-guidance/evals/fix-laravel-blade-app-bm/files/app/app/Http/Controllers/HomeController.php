<?php
namespace App\Http\Controllers;

use App\Models\News;

class HomeController extends Controller
{
    public function index()
    {
        return view('home', ['latestNews' => News::latest('published_at')->first()]);
    }
}
