"""End-to-end verification script for PlantHealthApp."""

import sys
import os
from pathlib import Path

# Add project root to sys.path
BASE_DIR = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(BASE_DIR))

from starlette.testclient import TestClient
from app.backend.main import app
from app.backend.database import get_all_analyses

def main():
    print("=" * 60)
    print("RUNNING COMPLETE ACCEPTANCE TEST SUITE (PLANT HEALTH APP)")
    print("=" * 60)

    with TestClient(app) as client:
        # 1. Health check
        res = client.get("/api/health")
        assert res.status_code == 200, f"Health check status: {res.status_code}"
        h = res.json()
        print(f"[TEST 1/7] Health check: OK (Model loaded={h['model_loaded']}, Classes count={h['classes_count']}, DB OK={h['database_ok']})")
        assert h["status"] == "ok"
        assert h["model_loaded"] is True
        assert h["database_ok"] is True
        assert h["classes_count"] == 38

        # 2. Connection Info
        res = client.get("/api/connection-info")
        assert res.status_code == 200
        conn = res.json()
        print(f"[TEST 2/7] Connection info: OK (Mode={conn['mode']}, URL={conn['url']})")
        assert "url" in conn

        # 3. Diseases catalog
        res = client.get("/api/diseases")
        assert res.status_code == 200
        diseases = res.json()
        print(f"[TEST 3/7] Diseases catalog: OK ({len(diseases)} entries seeded in SQLite)")
        assert len(diseases) >= 38

        # 4. AutoSim execution (real TFLite inference)
        res = client.post("/api/autosim")
        assert res.status_code == 200
        auto = res.json()
        print(f"[TEST 4/7] AutoSim inference: OK")
        print(f"           Predicted: {auto['plant']} - {auto['display_name']}")
        print(f"           Confidence: {auto['confidence_percent']}%")
        print(f"           Simulated Flag: {auto['is_simulated']}")
        assert auto["is_simulated"] is True
        assert auto["confidence"] > 0.5
        assert len(auto["advice"]["description"]) > 20

        # 5. History persistence
        res = client.get("/api/history")
        assert res.status_code == 200
        history = res.json()
        print(f"[TEST 5/7] History persistence: OK ({len(history)} records in database)")
        assert len(history) > 0
        first_id = history[0]["id"]

        # 6. Delete test
        res = client.delete(f"/api/history/{first_id}")
        assert res.status_code == 200
        del_data = res.json()
        print(f"[TEST 6/7] History deletion: OK (Deleted ID={del_data.get('deleted_id')})")
        assert del_data.get("deleted_id") == first_id

        # 7. QR Vector endpoint
        res = client.get("/api/qr.svg")
        assert res.status_code == 200
        assert "svg" in res.headers.get("content-type", "").lower()
        print(f"[TEST 7/7] QR Code SVG endpoint: OK ({len(res.content)} bytes)")

        # Verify frontend assets serve properly
        res_index = client.get("/")
        assert res_index.status_code == 200
        assert "Plant Health Detection App" in res_index.text
        print("[TEST BONUS] Frontend SPA Index: OK (100% bundled locally)")

    print("=" * 60)
    print(">>> ALL 7 SYSTEM TESTS PASSED SUCCESSFULLY! <<<")
    print("=" * 60)

if __name__ == "__main__":
    main()
