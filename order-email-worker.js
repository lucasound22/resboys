// Cloudflare Worker - RES BOYS Order Email (for manual/demo checkout)
// Deploy separately: wrangler init res-boys-orders, paste, wrangler deploy
// This worker receives POST from GitHub Pages and emails you privately
// Frontend never shows your private email

const PRIVATE_OWNER_EMAIL = 'lucasound@gmail.com';

export default {
  async fetch(request, env, ctx) {
    if (request.method === 'OPTIONS') {
      return new Response(null, { headers: corsHeaders() });
    }
    if (request.method !== 'POST') {
      return new Response('RES BOYS Order Email Worker Live', { headers: corsHeaders() });
    }
    try {
      const data = await request.json();
      const { items, customer, total, mode } = data;

      const itemLines = (items||[]).map(it => {
        const p = it.name || it.id;
        return `• ${p} [${it.size}] x${it.qty} = $${((it.price||0)*it.qty/100 || it.price).toFixed ? '' : ''}${it.price ? (it.price/100*it.qty).toFixed(2) : it.total || ''} AUD`;
      }).join('\n');

      // Better formatting
      const prettyItems = (items||[]).map(it => {
        const name = it.name || it.id;
        const price = it.price ? `$${(it.price/100).toFixed(2)}` : (it.total || '');
        return `${name} [${it.size}] x${it.qty} — ${price}`;
      }).join('\n');

      const subject = `NEW RES BOYS ORDER — ${customer?.email || 'Guest'} — ${total || ''} AUD`;

      const text = `NEW ORDER — DROP 01 / SS26

Mode: ${mode || 'demo/manual'}

Items:
${prettyItems}

Subtotal/Total: ${total || 'See items'}

Customer:
${customer?.first || ''} ${customer?.last || ''}
${customer?.email || ''}
${customer?.address || ''}
${customer?.city || ''} ${customer?.postcode || ''}
Shipping: ${customer?.shipping || 'Standard'}

Time: ${new Date().toISOString()}

— Sent from resboys.com.au checkout (GitHub Pages)
Private notification — do not reply to customer from this address unless you want to.
`;

      // Send via MailChannels
      const emailRes = await fetch('https://api.mailchannels.net/tx/v1/send', {
        method: 'POST',
        headers: { 'content-type': 'application/json' },
        body: JSON.stringify({
          personalizations: [{ to: [{ email: PRIVATE_OWNER_EMAIL, name: 'RES BOYS Orders' }] }],
          from: { email: 'orders@resboys.com.au', name: 'RES BOYS Store' },
          subject,
          content: [{ type: 'text/plain', value: text }],
          reply_to: customer?.email ? { email: customer.email, name: `${customer.first||''} ${customer.last||''}` } : undefined
        })
      });

      const result = await emailRes.text();
      return json({ ok: true, mailchannels: result });
    } catch (e) {
      return json({ error: e.message }, 500);
    }
  }
};

function corsHeaders(){
  return {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'POST, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type',
  };
}
function json(data, status=200){
  return new Response(JSON.stringify(data), {status, headers:{'Content-Type':'application/json', ...corsHeaders()}});
}
