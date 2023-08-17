import requests

ENDPOINT = "sem-search-score"

def test_similarity(url):
    "test the similarity between two different tech"
    javascript_search_url = url + ENDPOINT + '/javascript'
    get_javascript = requests.get(url=javascript_search_url)
    javascript_java_angle = [ tech['java'] for tech in get_javascript.json() if 'java' in tech.keys()]
    print(javascript_java_angle)

    java_search_url = url + ENDPOINT + '/java'
    get_java = requests.get(url=java_search_url)
    java_javascript_angle = [ tech['javascript'] for tech in get_java.json() if 'javascript' in tech.keys()]
    print(java_javascript_angle)

    assert javascript_java_angle == java_javascript_angle