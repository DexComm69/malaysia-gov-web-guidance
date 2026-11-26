<?php
use App\Http\Controllers\HomeController;
use App\Http\Controllers\PageController;
use App\Http\Controllers\FeedbackController;
use Illuminate\Support\Facades\Route;

Route::get('/', [HomeController::class, 'index']);
Route::get('/maklum-balas', [FeedbackController::class, 'create']);
Route::post('/maklum-balas', [FeedbackController::class, 'store']);
Route::get('/carian', [PageController::class, 'search']);
Route::get('/{slug}', [PageController::class, 'show']);
