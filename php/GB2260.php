<?php

class GB2260{
	protected static $_data;

	public static function getData(){
		if (empty(self::$_data))
			self::$_data = require 'data.php';
		return self::$_data;
	}

	public static function parse($code){
		if (empty(self::$_data))
			self::$_data = require 'data.php';

		$code = preg_replace('/0+$/', '', $code);
		$codeLength = strlen($code);
		if ($codeLength < 2 || $codeLength > 6 || $codeLength % 2 !== 0) {
			throw new Exception('Invalid code');
		}

		$province = self::$_data[substr($code, 0, 2) . '0000'];
		if (!$province) return null;

		if ($codeLength === 2) {
			return $province;
		}

		$area = self::$_data[substr($code, 0, 4) . '00'];
		if (!$area) return null;

		if ($codeLength === 4) {
			return $province . ' ' . $area;
		}

		$name = self::$_data[$code];
		if (!$name) return null;

		return $province . ' ' . $area . ' ' . $name;
	}
}

