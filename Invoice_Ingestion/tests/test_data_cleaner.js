// test_data_cleaner.js
// This script contains the logic used in the n8n Code node to clean and validate AI output.
// Run with Node.js: `node test_data_cleaner.js`

function cleanAndValidate(aiJsonString) {
    let data;
    try {
        data = JSON.parse(aiJsonString);
    } catch (e) {
        return { error: "Failed to parse JSON", raw: aiJsonString };
    }

    // Default Fallbacks
    const cleaned = {
        vendor: data.vendor || "Unknown Vendor",
        vendor_uid: data.vendor_uid || null,
        vendor_iban: data.vendor_iban || null,
        invoice_number: data.invoice_number || `UNKNOWN-${Date.now()}`,
        invoice_date: data.invoice_date ? new Date(data.invoice_date).toISOString().split('T')[0] : null,
        due_date: data.due_date ? new Date(data.due_date).toISOString().split('T')[0] : null,
        net_amount: Math.max(0, parseFloat(data.net_amount) || 0),
        vat_amount: Math.max(0, parseFloat(data.vat_amount) || 0),
        vat_percent: Math.max(0, parseFloat(data.vat_percent) || 0),
        gross_amount: Math.max(0, parseFloat(data.gross_amount) || 0),
        currency: data.currency || "USD",
        cost_center: data.cost_center || "General",
        confidence_score: parseFloat(data.confidence_score) || 0,
        anomalies: Array.isArray(data.anomalies) ? data.anomalies : [],
        line_items: []
    };

    // Clean Line Items
    if (Array.isArray(data.line_items)) {
        cleaned.line_items = data.line_items.filter(item => {
            // Remove line items where description is empty or total <= 0
            if (!item.description || item.description.trim() === "") return false;
            const total = parseFloat(item.total) || 0;
            if (total <= 0) return false;
            return true;
        }).map(item => ({
            description: item.description.trim(),
            quantity: parseFloat(item.quantity) || 1,
            unit_price: parseFloat(item.unit_price) || 0,
            total: parseFloat(item.total) || 0
        }));
    }

    // Confidence Routing logic simulation
    if (cleaned.confidence_score < 0.7) {
        cleaned.anomalies.push("Low confidence score - requires supervisor review.");
        cleaned.status = "Needs Review";
    } else {
        cleaned.status = "Draft";
    }

    return cleaned;
}

// --- UNIT TESTS ---

const sampleGoodJson = JSON.stringify({
    "vendor": "Acme Supplies",
    "vendor_uid": "ACME123",
    "invoice_number": "INV-2026-001",
    "invoice_date": "2026-07-01",
    "net_amount": 1000.00,
    "vat_percent": 20,
    "gross_amount": 1200.00,
    "line_items": [
        { "description": "Laptops", "quantity": 10, "unit_price": 80, "total": 800 },
        { "description": "Monitors", "quantity": 5, "unit_price": 40, "total": 200 },
        { "description": "", "quantity": 0, "unit_price": 0, "total": 0 } // Should be filtered out
    ],
    "confidence_score": 0.85
});

const sampleBadJson = `{ "vendor": "Bad Corp", "net_amount": "invalid", "confidence_score": 0.5 }`;

console.log("--- Testing Good JSON ---");
const resultGood = cleanAndValidate(sampleGoodJson);
console.log(JSON.stringify(resultGood, null, 2));
console.assert(resultGood.line_items.length === 2, "Failed to filter empty line items");
console.assert(resultGood.status === "Draft", "Incorrect status for high confidence");

console.log("\n--- Testing Bad JSON ---");
const resultBad = cleanAndValidate(sampleBadJson);
console.log(JSON.stringify(resultBad, null, 2));
console.assert(resultBad.net_amount === 0, "Failed to default invalid net amount to 0");
console.assert(resultBad.status === "Needs Review", "Incorrect status for low confidence");
console.assert(resultBad.anomalies.length > 0, "Failed to add anomaly for low confidence");

console.log("\nTests completed.");
