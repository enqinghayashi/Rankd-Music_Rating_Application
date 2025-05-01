"""
JSON returned from running api.search("The Black Parade", 0, 1).

Contains 1 Track, 1 Album, and 1 Artist.
"""
data = {
  'tracks': {
    'href': 'https://api.spotify.com/v1/search?offset=0&limit=1&query=The%20Black%20Parade&type=track', 
    'limit': 1, 
    'next': 'https://api.spotify.com/v1/search?offset=1&limit=1&query=The%20Black%20Parade&type=track', 
    'offset': 0, 
    'previous': None, 
    'total': 1000, 
    'items': [
      {
        'album': {
          'album_type': 'album', 
          'artists': [
            {'external_urls': {'spotify': 'https://open.spotify.com/artist/7FBcuc1gsnv6Y1nwFtNRCb'}, 
             'href': 'https://api.spotify.com/v1/artists/7FBcuc1gsnv6Y1nwFtNRCb', 
             'id': '7FBcuc1gsnv6Y1nwFtNRCb', 
             'name': 'My Chemical Romance', 
             'type': 'artist', 
             'uri': 'spotify:artist:7FBcuc1gsnv6Y1nwFtNRCb'
            }
          ], 
          'available_markets': ['AR', 'AU', 'AT', 'BE', 'BO', 'BR', 'BG', 'CA', 'CL', 'CO', 'CR', 'CY', 'CZ', 'DK', 'DO', 'DE', 'EC', 'EE', 'SV', 'FI', 'FR', 'GR', 'GT', 'HN', 'HK', 'HU', 'IS', 'IE', 'IT', 'LV', 'LT', 'LU', 'MY', 'MT', 'MX', 'NL', 'NZ', 'NI', 'NO', 'PA', 'PY', 'PE', 'PH', 'PL', 'PT', 'SG', 'SK', 'ES', 'SE', 'CH', 'TW', 'TR', 'UY', 'US', 'GB', 'AD', 'LI', 'MC', 'ID', 'JP', 'TH', 'VN', 'RO', 'IL', 'ZA', 'SA', 'AE', 'BH', 'QA', 'OM', 'KW', 'EG', 'MA', 'DZ', 'TN', 'LB', 'JO', 'PS', 'IN', 'BY', 'KZ', 'MD', 'UA', 'AL', 'BA', 'HR', 'ME', 'MK', 'RS', 'SI', 'KR', 'BD', 'PK', 'LK', 'GH', 'KE', 'NG', 'TZ', 'UG', 'AG', 'AM', 'BS', 'BB', 'BZ', 'BT', 'BW', 'BF', 'CV', 'CW', 'DM', 'FJ', 'GM', 'GE', 'GD', 'GW', 'GY', 'HT', 'JM', 'KI', 'LS', 'LR', 'MW', 'MV', 'ML', 'MH', 'FM', 'NA', 'NR', 'NE', 'PW', 'PG', 'PR', 'WS', 'SM', 'ST', 'SN', 'SC', 'SL', 'SB', 'KN', 'LC', 'VC', 'SR', 'TL', 'TO', 'TT', 'TV', 'VU', 'AZ', 'BN', 'BI', 'KH', 'CM', 'TD', 'KM', 'GQ', 'SZ', 'GA', 'GN', 'KG', 'LA', 'MO', 'MR', 'MN', 'NP', 'RW', 'TG', 'UZ', 'ZW', 'BJ', 'MG', 'MU', 'MZ', 'AO', 'CI', 'DJ', 'ZM', 'CD', 'CG', 'IQ', 'LY', 'TJ', 'VE', 'ET', 'XK'], 
          'external_urls': {'spotify': 'https://open.spotify.com/album/0FZK97MXMm5mUQ8mtudjuK'}, 
          'href': 'https://api.spotify.com/v1/albums/0FZK97MXMm5mUQ8mtudjuK', 
          'id': '0FZK97MXMm5mUQ8mtudjuK', 
          'images': [
            {'height': 640, 'width': 640, 'url': 'https://i.scdn.co/image/ab67616d0000b27317f77fab7e8f18d5f9fee4a1'}, 
            {'height': 300, 'width': 300, 'url': 'https://i.scdn.co/image/ab67616d00001e0217f77fab7e8f18d5f9fee4a1'}, 
            {'height': 64, 'width': 64, 'url': 'https://i.scdn.co/image/ab67616d0000485117f77fab7e8f18d5f9fee4a1'}
          ], 
          'is_playable': True, 
          'name': 'The Black Parade', 
          'release_date': '2006-10-20', 
          'release_date_precision': 'day', 
          'total_tracks': 14, 
          'type': 'album', 
          'uri': 'spotify:album:0FZK97MXMm5mUQ8mtudjuK'
        }, 
        'artists': [
          {
            'external_urls': {'spotify': 'https://open.spotify.com/artist/7FBcuc1gsnv6Y1nwFtNRCb'}, 
            'href': 'https://api.spotify.com/v1/artists/7FBcuc1gsnv6Y1nwFtNRCb', 
            'id': '7FBcuc1gsnv6Y1nwFtNRCb', 
            'name': 'My Chemical Romance', 
            'type': 'artist', 
            'uri': 'spotify:artist:7FBcuc1gsnv6Y1nwFtNRCb'
          }
        ], 
        'available_markets': ['AR', 'AU', 'AT', 'BE', 'BO', 'BR', 'BG', 'CA', 'CL', 'CO', 'CR', 'CY', 'CZ', 'DK', 'DO', 'DE', 'EC', 'EE', 'SV', 'FI', 'FR', 'GR', 'GT', 'HN', 'HK', 'HU', 'IS', 'IE', 'IT', 'LV', 'LT', 'LU', 'MY', 'MT', 'MX', 'NL', 'NZ', 'NI', 'NO', 'PA', 'PY', 'PE', 'PH', 'PL', 'PT', 'SG', 'SK', 'ES', 'SE', 'CH', 'TW', 'TR', 'UY', 'US', 'GB', 'AD', 'LI', 'MC', 'ID', 'JP', 'TH', 'VN', 'RO', 'IL', 'ZA', 'SA', 'AE', 'BH', 'QA', 'OM', 'KW', 'EG', 'MA', 'DZ', 'TN', 'LB', 'JO', 'PS', 'IN', 'BY', 'KZ', 'MD', 'UA', 'AL', 'BA', 'HR', 'ME', 'MK', 'RS', 'SI', 'KR', 'BD', 'PK', 'LK', 'GH', 'KE', 'NG', 'TZ', 'UG', 'AG', 'AM', 'BS', 'BB', 'BZ', 'BT', 'BW', 'BF', 'CV', 'CW', 'DM', 'FJ', 'GM', 'GE', 'GD', 'GW', 'GY', 'HT', 'JM', 'KI', 'LS', 'LR', 'MW', 'MV', 'ML', 'MH', 'FM', 'NA', 'NR', 'NE', 'PW', 'PG', 'PR', 'WS', 'SM', 'ST', 'SN', 'SC', 'SL', 'SB', 'KN', 'LC', 'VC', 'SR', 'TL', 'TO', 'TT', 'TV', 'VU', 'AZ', 'BN', 'BI', 'KH', 'CM', 'TD', 'KM', 'GQ', 'SZ', 'GA', 'GN', 'KG', 'LA', 'MO', 'MR', 'MN', 'NP', 'RW', 'TG', 'UZ', 'ZW', 'BJ', 'MG', 'MU', 'MZ', 'AO', 'CI', 'DJ', 'ZM', 'CD', 'CG', 'IQ', 'LY', 'TJ', 'VE', 'ET', 'XK'], 
        'disc_number': 1, 
        'duration_ms': 311106, 
        'explicit': False, 
        'external_ids': {'isrc': 'USRE10602613'}, 
        'external_urls': {'spotify': 'https://open.spotify.com/track/5wQnmLuC1W7ATsArWACrgW'}, 
        'href': 'https://api.spotify.com/v1/tracks/5wQnmLuC1W7ATsArWACrgW', 
        'id': '5wQnmLuC1W7ATsArWACrgW', 
        'is_local': False, 
        'is_playable': True, 
        'name': 'Welcome to the Black Parade', 
        'popularity': 80, 
        'preview_url': None, 
        'track_number': 5, 
        'type': 'track', 
        'uri': 'spotify:track:5wQnmLuC1W7ATsArWACrgW'
      }
    ]
  }, 
  'artists': {
    'href': 'https://api.spotify.com/v1/search?offset=0&limit=1&query=The%20Black%20Parade&type=artist', 
    'limit': 1, 
    'next': 'https://api.spotify.com/v1/search?offset=1&limit=1&query=The%20Black%20Parade&type=artist', 
    'offset': 0, 
    'previous': None, 
    'total': 802, 
    'items': [
      {
        'external_urls': {'spotify': 'https://open.spotify.com/artist/7FBcuc1gsnv6Y1nwFtNRCb'}, 
        'followers': {'href': None, 'total': 9674260}, 
        'genres': ['emo', 'pop punk', 'emo pop'], 
        'href': 'https://api.spotify.com/v1/artists/7FBcuc1gsnv6Y1nwFtNRCb', 
        'id': '7FBcuc1gsnv6Y1nwFtNRCb', 
        'images': [
          {'url': 'https://i.scdn.co/image/ab6761610000e5eb9c00ad0308287b38b8fdabc2', 'height': 640, 'width': 640}, 
          {'url': 'https://i.scdn.co/image/ab676161000051749c00ad0308287b38b8fdabc2', 'height': 320, 'width': 320}, 
          {'url': 'https://i.scdn.co/image/ab6761610000f1789c00ad0308287b38b8fdabc2', 'height': 160, 'width': 160}
        ], 
        'name': 'My Chemical Romance', 
        'popularity': 80, 
        'type': 'artist', 
        'uri': 'spotify:artist:7FBcuc1gsnv6Y1nwFtNRCb'
      }
    ]
  }, 
  'albums': {
    'href': 'https://api.spotify.com/v1/search?offset=0&limit=1&query=The%20Black%20Parade&type=album', 
    'limit': 1, 
    'next': 'https://api.spotify.com/v1/search?offset=1&limit=1&query=The%20Black%20Parade&type=album', 
    'offset': 0, 
    'previous': None, 
    'total': 899, 
    'items': [
      {
        'album_type': 'album', 
        'total_tracks': 14, 
        'available_markets': ['AR', 'AU', 'AT', 'BE', 'BO', 'BR', 'BG', 'CA', 'CL', 'CO', 'CR', 'CY', 'CZ', 'DK', 'DO', 'DE', 'EC', 'EE', 'SV', 'FI', 'FR', 'GR', 'GT', 'HN', 'HK', 'HU', 'IS', 'IE', 'IT', 'LV', 'LT', 'LU', 'MY', 'MT', 'MX', 'NL', 'NZ', 'NI', 'NO', 'PA', 'PY', 'PE', 'PH', 'PL', 'PT', 'SG', 'SK', 'ES', 'SE', 'CH', 'TW', 'TR', 'UY', 'US', 'GB', 'AD', 'LI', 'MC', 'ID', 'JP', 'TH', 'VN', 'RO', 'IL', 'ZA', 'SA', 'AE', 'BH', 'QA', 'OM', 'KW', 'EG', 'MA', 'DZ', 'TN', 'LB', 'JO', 'PS', 'IN', 'BY', 'KZ', 'MD', 'UA', 'AL', 'BA', 'HR', 'ME', 'MK', 'RS', 'SI', 'KR', 'BD', 'PK', 'LK', 'GH', 'KE', 'NG', 'TZ', 'UG', 'AG', 'AM', 'BS', 'BB', 'BZ', 'BT', 'BW', 'BF', 'CV', 'CW', 'DM', 'FJ', 'GM', 'GE', 'GD', 'GW', 'GY', 'HT', 'JM', 'KI', 'LS', 'LR', 'MW', 'MV', 'ML', 'MH', 'FM', 'NA', 'NR', 'NE', 'PW', 'PG', 'PR', 'WS', 'SM', 'ST', 'SN', 'SC', 'SL', 'SB', 'KN', 'LC', 'VC', 'SR', 'TL', 'TO', 'TT', 'TV', 'VU', 'AZ', 'BN', 'BI', 'KH', 'CM', 'TD', 'KM', 'GQ', 'SZ', 'GA', 'GN', 'KG', 'LA', 'MO', 'MR', 'MN', 'NP', 'RW', 'TG', 'UZ', 'ZW', 'BJ', 'MG', 'MU', 'MZ', 'AO', 'CI', 'DJ', 'ZM', 'CD', 'CG', 'IQ', 'LY', 'TJ', 'VE', 'ET', 'XK'], 
        'external_urls': {'spotify': 'https://open.spotify.com/album/0FZK97MXMm5mUQ8mtudjuK'}, 
        'href': 'https://api.spotify.com/v1/albums/0FZK97MXMm5mUQ8mtudjuK', 
        'id': '0FZK97MXMm5mUQ8mtudjuK', 
        'images': [
          {'height': 640, 'url': 'https://i.scdn.co/image/ab67616d0000b27317f77fab7e8f18d5f9fee4a1', 'width': 640}, 
          {'height': 300, 'url': 'https://i.scdn.co/image/ab67616d00001e0217f77fab7e8f18d5f9fee4a1', 'width': 300}, 
          {'height': 64, 'url': 'https://i.scdn.co/image/ab67616d0000485117f77fab7e8f18d5f9fee4a1', 'width': 64}
        ], 
        'name': 'The Black Parade', 
        'release_date': '2006-10-20', 
        'release_date_precision': 'day', 
        'type': 'album', 
        'uri': 'spotify:album:0FZK97MXMm5mUQ8mtudjuK', 
        'artists': [
          {
            'external_urls': {'spotify': 'https://open.spotify.com/artist/7FBcuc1gsnv6Y1nwFtNRCb'}, 
            'href': 'https://api.spotify.com/v1/artists/7FBcuc1gsnv6Y1nwFtNRCb', 
            'id': '7FBcuc1gsnv6Y1nwFtNRCb', 
            'name': 'My Chemical Romance', 
            'type': 'artist', 
            'uri': 'spotify:artist:7FBcuc1gsnv6Y1nwFtNRCb'
          }
        ]
      }
    ]
  }
}