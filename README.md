# Saltstack Netlify

Salt modules to deal with Netlify.

(This module depends on `requests`.)


## Install

 * Copy `netlify.py` to **/src/salt/_states**.
 * Run `sudo salt-call saltutil.sync_states` to send the
 file to the minions


## Usage

### Netlify access key

 * Login into Netlify website (`https://app.netlify.com/`).
 * Access `https://app.netlify.com/account/applications`.
 * Click the button `New access token`.
 * Copy and save in a safe place your new access token.

### A proper pillar

For example: `/srv/pillar/netlify.sls`.


```yaml
netlify:
  access_token: "<YOUR-ACCESS-TOKEN>"
  sites:
    <SITE-NAME>:
      id: "<SITE-ID>"
```


Remember to add `netlify' to your `/srv/pillar/top.sls`!

### Salt state file

```yaml

{% set site_id = salt.pillar.get('netlify:sites:<SITE-NAME>:id') %}
{% set access_token = salt.pillar.get('netlify:access_token') %}

netlify_<SITE-NAME>_aliases:
  netlify.aliases_present:
    - access_token: "{{ access_token }}"
      site_id: "{{ site_id }}"
      aliases:
        - "<SOME.DOMAIN.EXAMPLE.COM>",
        - "<AND.YET.ANOTHER.DOMAIN.EXAMPLE.COM>",
```
