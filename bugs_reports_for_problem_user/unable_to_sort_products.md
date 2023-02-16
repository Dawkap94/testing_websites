### Manual test Saucedemo.com functionality for username "problem_user"

|          Title          | Operation system | Environment |   Issue type    |  Severity  | Frequency  |   Source   |
|:-----------------------:|:----------------:|:-----------:|:---------------:|:----------:|:----------:|:----------:|
| Unable to sort products | Windows 10 Pro   | Chrome(x64) |   Functional    |    High    | Every time | Structured |

#### Action Performed
 1. Visit https://www.saucedemo.com/
 2. Login as username:problem_user, password:secret_sauce to see PLP
 3. Click on sorting panel on the right upper part of PLP
 4. Select "Price (low to high)"

#### Expected result:
I expected to sort product by price.

#### Actual result:
Products are not sorted.

#### Image:
![](https://i.ibb.co/N9YZDFM/sorting-problem.jpg)

#### Chrome Logs:
>17:20:20.724 DevTools failed to load source map: Could not load content for chrome-extension://gighmmpiobklfepjocnamgkkbiglidom/browser-polyfill.js.map: Fetch through target failed: Frame not found; Fallback: HTTP error: status code 404, net::ERR_UNKNOWN_URL_SCHEME
