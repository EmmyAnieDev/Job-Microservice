<?php

namespace App\Facades;

use Illuminate\Support\Facades\Facade;

class JwtService extends Facade
{
    protected static function getFacadeAccessor()
    {
        return 'JwtService';
    }
}
