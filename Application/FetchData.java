import org.json.JSONArray;
import org.json.JSONObject;

public class FetchData {

	public static void main(String[] args) {
		
		communication con = new communication();
		Boolean res = con.connect("", 1024);
//		String jsonStr = "{\"type\": 1, \"name\": \"Database\", \"data\": {\"method\": \"get\", \"command\": \"all_vehicle_info\"}}";
		JSONObject request = new JSONObject();
		JSONObject data = new JSONObject();
		data.put("method", "get");
		data.put("command", "all_vehicle_info");
		data.put("rego", "ABC123");
//		data.put("command", "vehicle_info");
		request.put("type", 1);
		request.put("name", "Database");
		request.put("data", data);
		con.sendMessage(request.toString());
		String result = con.getMessage();
		JSONArray response = new JSONArray(result);
		for (int i = 0; i < response.length(); i++) {
			JSONObject element = response.getJSONObject(i);
			//System.out.println(element.get("registration"));
		}
	}

}
