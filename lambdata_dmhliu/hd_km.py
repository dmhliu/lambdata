def hd(s):                                #need to accept series or list
    """function takes a series or list containing 2 coordinate pairs s=(lat1, lon1, lat2, lon2)
    returns the haversine distance between the two points represented in km
    """
    r = 6371
    phi1 = np.radians(s[0])
    phi2 = np.radians(s[2])
    delta_phi = np.radians(s[2] - s[0])
    delta_lambda = np.radians(s[3] - s[1])
    a = np.sin(delta_phi / 2)**2 + np.cos(phi1) * np.cos(phi2) *   np.sin(delta_lambda / 2)**2
    res = r * (2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a)))
    return np.round(res, 2)   #in km